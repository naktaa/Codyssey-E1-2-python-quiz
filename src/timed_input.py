import math
import os
import select
import sys
import time
from dataclasses import dataclass

try:
    import termios
except ImportError:  # pragma: no cover - macOS 외 플랫폼에서만 발생한다.
    termios = None


@dataclass(frozen=True)
class TimedAnswerResult:
    """시간 제한 입력의 답과 자동 힌트 공개 여부를 보관한다."""

    answer: int | None
    hint_shown: bool


class TimedTerminalInput:
    """macOS 터미널에서 카운트다운과 자동 힌트를 표시하며 답을 받는다."""

    TIME_LIMIT_SECONDS = 20.0
    HINT_DELAY_SECONDS = 10.0

    CLEAR_LINE = "\033[2K"
    CURSOR_UP_ONE_LINE = "\033[1A"
    CURSOR_DOWN_ONE_LINE = "\033[1B"

    def __init__(
        self,
        time_limit_seconds: float = TIME_LIMIT_SECONDS,
        hint_delay_seconds: float = HINT_DELAY_SECONDS,
    ) -> None:
        if time_limit_seconds <= 0:
            raise ValueError("제한 시간은 0초보다 커야 합니다.")
        if not 0 < hint_delay_seconds < time_limit_seconds:
            raise ValueError("힌트 시간은 0초보다 크고 제한 시간보다 작아야 합니다.")

        self.time_limit_seconds = time_limit_seconds
        self.hint_delay_seconds = hint_delay_seconds

    def read_answer(self, hint: str | None) -> TimedAnswerResult:
        """제한 시간 안에 1~4 답을 받고 설정된 시점에 힌트를 공개한다."""
        self._flush_pending_input()
        if self._supports_terminal_control():
            return self._read_interactive_answer(hint)
        return self._read_stream_answer(hint)

    def _read_interactive_answer(
        self,
        hint: str | None,
    ) -> TimedAnswerResult:
        """현재 줄만 다시 그리며 터미널에서 답을 한 글자씩 받는다."""
        started_at = time.monotonic()
        hint_at = started_at + self.hint_delay_seconds
        deadline = started_at + self.time_limit_seconds
        hint_shown = False
        remaining_seconds = math.ceil(self.time_limit_seconds)
        answer_buffer = ""
        error_line_visible = False
        input_line_finished = False
        original_settings = termios.tcgetattr(sys.stdin.fileno())
        input_settings = original_settings.copy()
        input_settings[6] = original_settings[6][:]
        input_settings[3] &= ~(termios.ICANON | termios.ECHO)
        input_settings[6][termios.VMIN] = 1
        input_settings[6][termios.VTIME] = 0

        print(self._hint_text(hint, hint_shown))
        self._draw_input_line(remaining_seconds, answer_buffer)
        termios.tcsetattr(
            sys.stdin.fileno(),
            termios.TCSANOW,
            input_settings,
        )

        try:
            while True:
                now = time.monotonic()
                if now >= deadline:
                    return TimedAnswerResult(answer=None, hint_shown=True)

                if not hint_shown and now >= hint_at:
                    hint_shown = True
                    self._replace_hint_line(hint)
                    self._draw_input_line(remaining_seconds, answer_buffer)

                new_remaining = math.ceil(deadline - now)
                if new_remaining != remaining_seconds:
                    remaining_seconds = new_remaining
                    self._draw_input_line(remaining_seconds, answer_buffer)

                next_tick_at = deadline - max(remaining_seconds - 1, 0)
                next_events = [next_tick_at, deadline]
                if not hint_shown:
                    next_events.append(hint_at)
                wait_seconds = max(0.0, min(next_events) - now)

                readable, _, _ = select.select(
                    [sys.stdin],
                    [],
                    [],
                    wait_seconds,
                )
                observed_at = time.monotonic()

                if observed_at >= deadline:
                    return TimedAnswerResult(answer=None, hint_shown=True)

                if not hint_shown and observed_at >= hint_at:
                    hint_shown = True
                    self._replace_hint_line(hint)
                    self._draw_input_line(remaining_seconds, answer_buffer)

                new_remaining = math.ceil(deadline - observed_at)
                if new_remaining != remaining_seconds:
                    remaining_seconds = new_remaining

                if not readable:
                    self._draw_input_line(remaining_seconds, answer_buffer)
                    continue

                raw_characters = os.read(sys.stdin.fileno(), 1024)
                if raw_characters == b"":
                    raise EOFError

                for character in raw_characters.decode(
                    errors="ignore",
                ):
                    if character in {"\x7f", "\b"}:
                        answer_buffer = answer_buffer[:-1]
                        self._draw_input_line(
                            remaining_seconds,
                            answer_buffer,
                        )
                        continue

                    if character not in {"\r", "\n"}:
                        if character.isprintable():
                            answer_buffer += character
                            self._draw_input_line(
                                remaining_seconds,
                                answer_buffer,
                            )
                        continue

                    submitted_at = time.monotonic()
                    if submitted_at >= deadline:
                        return TimedAnswerResult(
                            answer=None,
                            hint_shown=True,
                        )
                    if not hint_shown and submitted_at >= hint_at:
                        hint_shown = True
                        self._replace_hint_line(hint)
                        self._draw_input_line(
                            remaining_seconds,
                            answer_buffer,
                        )

                    answer_text = answer_buffer.strip()
                    if answer_text in {"1", "2", "3", "4"}:
                        self._finish_input_line(
                            remaining_seconds,
                            answer_text,
                            error_line_visible,
                        )
                        input_line_finished = True
                        return TimedAnswerResult(
                            answer=int(answer_text),
                            hint_shown=hint_shown,
                        )

                    answer_buffer = ""
                    remaining_seconds = math.ceil(
                        deadline - submitted_at
                    )
                    self._show_error_below_input(
                        "1부터 4 사이의 숫자를 입력해 주세요.",
                        error_line_visible,
                    )
                    error_line_visible = True
                    self._draw_input_line(
                        remaining_seconds,
                        answer_buffer,
                    )
        except (KeyboardInterrupt, EOFError):
            raise
        finally:
            termios.tcsetattr(
                sys.stdin.fileno(),
                termios.TCSANOW,
                original_settings,
            )
            self._flush_pending_input()
            if not input_line_finished:
                self._close_interactive_panel(error_line_visible)

    def _read_stream_answer(self, hint: str | None) -> TimedAnswerResult:
        """TTY가 아닌 입출력에서도 기존 줄 단위 입력을 지원한다."""
        started_at = time.monotonic()
        hint_at = started_at + self.hint_delay_seconds
        deadline = started_at + self.time_limit_seconds
        hint_shown = False
        remaining_seconds = math.ceil(self.time_limit_seconds)
        self._draw_panel(hint, hint_shown, remaining_seconds)

        try:
            while True:
                now = time.monotonic()
                if now >= deadline:
                    return self._timeout_result()

                if not hint_shown and now >= hint_at:
                    hint_shown = True
                    self._update_hint(hint)

                new_remaining = math.ceil(deadline - now)
                if new_remaining != remaining_seconds:
                    remaining_seconds = new_remaining

                next_tick_at = deadline - max(remaining_seconds - 1, 0)
                next_events = [next_tick_at, deadline]
                if not hint_shown:
                    next_events.append(hint_at)
                wait_seconds = max(0.0, min(next_events) - now)

                readable, _, _ = select.select(
                    [sys.stdin],
                    [],
                    [],
                    wait_seconds,
                )
                observed_at = time.monotonic()

                if observed_at >= deadline:
                    return self._timeout_result()

                if not hint_shown and observed_at >= hint_at:
                    hint_shown = True
                    self._update_hint(hint)

                if not readable:
                    continue

                raw_answer = sys.stdin.readline()
                if raw_answer == "":
                    raise EOFError

                submitted_at = time.monotonic()
                if submitted_at >= deadline:
                    return self._timeout_result()

                if not hint_shown and submitted_at >= hint_at:
                    hint_shown = True
                    self._update_hint(hint)

                answer_text = raw_answer.strip()
                if answer_text in {"1", "2", "3", "4"}:
                    self._finish_submitted_line()
                    return TimedAnswerResult(
                        answer=int(answer_text),
                        hint_shown=hint_shown,
                    )

                self._finish_submitted_line()
                print("1부터 4 사이의 숫자를 입력해 주세요.")
                remaining_seconds = math.ceil(deadline - submitted_at)
                self._draw_panel(hint, hint_shown, remaining_seconds)
        except (KeyboardInterrupt, EOFError):
            self._close_prompt(clear_line=True)
            raise

    def _draw_panel(
        self,
        hint: str | None,
        hint_shown: bool,
        remaining_seconds: int,
    ) -> None:
        print(self._hint_text(hint, hint_shown))
        print(f"남은 시간: {remaining_seconds}초")
        print("정답 번호(1~4): ", end="", flush=True)

    def _update_hint(self, hint: str | None) -> None:
        print("")
        print(self._hint_text(hint, hint_shown=True))
        print("정답 번호(1~4): ", end="", flush=True)

    def _draw_input_line(
        self,
        remaining_seconds: int,
        answer_buffer: str,
    ) -> None:
        sys.stdout.write(
            f"\r{self.CLEAR_LINE}남은 시간: {remaining_seconds}초"
            f" | 정답 번호(1~4): {answer_buffer}"
        )
        sys.stdout.flush()

    def _replace_hint_line(self, hint: str | None) -> None:
        """현재 입력 줄을 유지하며 바로 위의 힌트 줄만 교체한다."""
        sys.stdout.write(
            f"\r{self.CLEAR_LINE}{self.CURSOR_UP_ONE_LINE}\r"
            f"{self.CLEAR_LINE}{self._hint_text(hint, hint_shown=True)}"
            f"{self.CURSOR_DOWN_ONE_LINE}\r"
        )
        sys.stdout.flush()

    def _finish_input_line(
        self,
        remaining_seconds: int,
        answer_text: str,
        error_line_visible: bool,
    ) -> None:
        self._draw_input_line(remaining_seconds, answer_text)
        if error_line_visible:
            sys.stdout.write(f"\r\n{self.CLEAR_LINE}\r\n")
        else:
            sys.stdout.write("\r\n")
        sys.stdout.flush()

    def _show_error_below_input(
        self,
        message: str,
        error_line_visible: bool,
    ) -> None:
        """입력 줄 아래의 오류 전용 줄을 만들거나 같은 자리에서 갱신한다."""
        if error_line_visible:
            sys.stdout.write(self.CURSOR_DOWN_ONE_LINE)
        else:
            sys.stdout.write("\r\n")

        sys.stdout.write(
            f"\r{self.CLEAR_LINE}{message}"
            f"{self.CURSOR_UP_ONE_LINE}\r"
        )
        sys.stdout.flush()

    def _close_interactive_panel(self, error_line_visible: bool) -> None:
        """입력과 선택적 오류 줄을 정리하고 패널 다음 줄로 이동한다."""
        self._clear_current_line()
        if error_line_visible:
            sys.stdout.write(
                f"{self.CURSOR_DOWN_ONE_LINE}\r{self.CLEAR_LINE}"
            )
        sys.stdout.write("\r\n")
        sys.stdout.flush()

    def _clear_current_line(self) -> None:
        sys.stdout.write(f"\r{self.CLEAR_LINE}")
        sys.stdout.flush()

    def _hint_text(self, hint: str | None, hint_shown: bool) -> str:
        if not hint_shown:
            return "힌트:"
        if hint is None:
            return "힌트: 등록된 힌트가 없습니다."
        return f"힌트: {hint}"

    def _timeout_result(self) -> TimedAnswerResult:
        self._flush_pending_input()
        self._close_prompt(clear_line=True)
        return TimedAnswerResult(answer=None, hint_shown=True)

    def _flush_pending_input(self) -> None:
        if termios is None or not sys.stdin.isatty():
            return

        try:
            termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)
        except (OSError, ValueError):
            pass

    def _close_prompt(self, clear_line: bool) -> None:
        if self._supports_terminal_control():
            if clear_line:
                sys.stdout.write(f"\r{self.CLEAR_LINE}")
            sys.stdout.write("\n")
            sys.stdout.flush()
            return

        print("")

    def _finish_submitted_line(self) -> None:
        print("")

    @staticmethod
    def _supports_terminal_control() -> bool:
        return (
            termios is not None
            and sys.stdin.isatty()
            and sys.stdout.isatty()
        )
