import random
from datetime import datetime

from .quiz import Quiz
from .state_manager import ScoreRecord, StateManager
from .timed_input import TimedTerminalInput


class GameManager:
    """터미널 퀴즈 게임의 메뉴와 공통 입력을 관리한다."""

    CORRECT_POINTS = 3
    HINT_PENALTY = 2
    SECTION_LINE = "=" * 40
    DETAIL_LINE = "-" * 40

    MENU_ITEMS = {
        1: "퀴즈 풀기",
        2: "퀴즈 목록 보기",
        3: "최고 점수와 기록",
        4: "퀴즈 추가",
        5: "퀴즈 삭제",
        6: "종료",
    }

    def __init__(self, state_manager: StateManager) -> None:
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.score_history: list[ScoreRecord] = []
        self.state_manager = state_manager
        self.timed_input = TimedTerminalInput()

    def show_section(self, title: str) -> None:
        """메뉴와 기능의 시작 위치를 같은 형식으로 구분한다."""
        print("")
        print(self.SECTION_LINE)
        print(title)
        print(self.SECTION_LINE)

    def show_menu(self) -> None:
        self.show_section("상식 퀴즈 게임")
        score_text = (
            "기록 없음"
            if self.best_score is None
            else f"{self.best_score}점"
        )
        print(f"등록 문제: {len(self.quizzes)}개 | 최고 점수: {score_text}")
        print(self.DETAIL_LINE)
        for number, label in self.MENU_ITEMS.items():
            print(f"{number}. {label}")
        print(self.DETAIL_LINE)

    def read_int(self, prompt: str, minimum: int, maximum: int) -> int:
        """지정된 범위의 정수가 입력될 때까지 다시 입력받는다."""
        while True:
            raw_value = input(prompt).strip()

            if not raw_value:
                print("입력값이 비어 있습니다. 숫자를 입력해 주세요.")
                continue

            try:
                value = int(raw_value)
            except ValueError:
                print("숫자만 입력해 주세요.")
                continue

            if minimum <= value <= maximum:
                return value

            print(f"{minimum}부터 {maximum} 사이의 숫자를 입력해 주세요.")

    def read_nonempty(self, prompt: str) -> str:
        """공백이 아닌 문자열이 입력될 때까지 다시 입력받는다."""
        while True:
            value = input(prompt).strip()
            if value:
                return value

            print("입력값이 비어 있습니다. 내용을 입력해 주세요.")

    def read_yes_no(self, prompt: str) -> bool:
        """y 또는 n이 입력될 때까지 다시 입력받는다."""
        while True:
            answer = input(prompt).strip().casefold()
            if answer == "y":
                return True
            if answer == "n":
                return False
            print("y 또는 n을 입력해 주세요.")

    def save_state(self) -> bool:
        """현재 게임 상태를 StateManager에 전달해 저장한다."""
        return self.state_manager.save_state(
            self.quizzes,
            self.best_score,
            self.score_history,
        )

    def load_state(self) -> None:
        """StateManager에서 상태를 불러와 현재 게임에 반영한다."""
        (
            self.quizzes,
            self.best_score,
            self.score_history,
        ) = self.state_manager.load_state()

    def add_quiz(self) -> bool:
        """새 퀴즈를 추가하고 저장하며 실패하면 메모리 변경을 되돌린다."""
        self.show_section("퀴즈 추가")
        question = self.read_nonempty("문제: ")
        choices = [
            self.read_nonempty(f"선택지 {number}: ")
            for number in range(1, 5)
        ]
        answer = self.read_int("정답 번호(1~4): ", 1, 4)
        hint = self.read_nonempty("힌트: ")

        new_quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint,
        )
        self.quizzes.append(new_quiz)

        if self.save_state():
            print("퀴즈를 추가하고 저장했습니다.")
            return True

        self.quizzes.pop()
        print("파일에 저장하지 못해 퀴즈 추가를 취소했습니다.")
        return False

    def list_quizzes(self) -> None:
        """저장된 상식 퀴즈의 번호와 질문을 연속해서 출력한다."""
        self.show_section("퀴즈 목록")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"총 {len(self.quizzes)}개의 문제가 등록되어 있습니다.")
        print(self.DETAIL_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def delete_quiz(self) -> bool:
        """선택한 퀴즈를 확인 후 삭제하고 상태 파일에 저장한다."""
        self.show_section("퀴즈 삭제")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return False

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")
        print(self.DETAIL_LINE)

        choice = self.read_int(
            "삭제할 문제 번호를 입력하세요: ",
            1,
            len(self.quizzes),
        )
        quiz_index = choice - 1
        selected_quiz = self.quizzes[quiz_index]
        print(f"삭제할 문제: {selected_quiz.question}")
        if not self.read_yes_no("정말 삭제하시겠습니까? (y/n): "):
            print("퀴즈 삭제를 취소했습니다.")
            return False

        self.quizzes.pop(quiz_index)

        if self.save_state():
            print("퀴즈를 삭제하고 저장했습니다.")
            return True

        self.quizzes.insert(quiz_index, selected_quiz)
        print("파일에 저장하지 못해 퀴즈 삭제를 취소했습니다.")
        return False

    def play_quizzes(self) -> int | None:
        """전체 상식 퀴즈를 자동 힌트가 있는 제한 시간 방식으로 출제한다."""
        self.show_section("퀴즈 풀기")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return None

        total_quizzes = len(self.quizzes)
        print(f"등록된 상식 퀴즈는 총 {total_quizzes}문제입니다.")
        quiz_count = self.read_int(
            f"풀 문제 수를 입력하세요(1~{total_quizzes}): ",
            1,
            total_quizzes,
        )
        # 원본 저장 순서는 유지하고 이번 플레이의 출제 목록만 무작위로 만든다.
        selected_quizzes = random.sample(self.quizzes, k=quiz_count)
        correct_count = 0
        hint_count = 0
        score = 0
        total_count = len(selected_quizzes)

        self.show_section("상식 퀴즈 시작")
        print(f"선택한 문제: {total_count}개")
        print(
            f"제한 시간: {self.timed_input.time_limit_seconds:g}초 | "
            f"힌트: {self.timed_input.hint_delay_seconds:g}초 후 공개"
        )
        for number, quiz in enumerate(selected_quizzes, start=1):
            print("")
            print(self.DETAIL_LINE)
            print(f"[문제 {number}/{total_count}]")
            quiz.display()
            answer_result = self.timed_input.read_answer(quiz.hint)
            if answer_result.hint_shown:
                hint_count += 1

            if answer_result.answer is None:
                print("시간 초과입니다. 0점입니다.")
                continue

            if quiz.is_correct(answer_result.answer):
                correct_count += 1
                hint_penalty = (
                    self.HINT_PENALTY
                    if answer_result.hint_shown
                    else 0
                )
                earned_points = self.CORRECT_POINTS - hint_penalty
                score += earned_points
                print(f"정답입니다! {earned_points}점을 획득했습니다.")
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                print(
                    f"오답입니다. 정답은 {quiz.answer}번 {correct_choice}입니다."
                )

        self.show_section("퀴즈 결과")
        print(f"정답 수: {correct_count}/{total_count}")
        print(f"힌트 사용 횟수: {hint_count}회")
        print(f"최종 점수: {score}점")
        if self.record_game_result(score):
            print(f"새로운 최고 점수: {score}점")
        return score

    def record_game_result(self, score: int) -> bool:
        """완료한 플레이를 기록하고 최고 점수와 함께 한 번 저장한다."""
        previous_score = self.best_score
        is_new_best = self.best_score is None or score > self.best_score
        if is_new_best:
            self.best_score = score

        record: ScoreRecord = {
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "score": score,
        }
        self.score_history.append(record)

        if self.save_state():
            return is_new_best

        self.score_history.pop()
        self.best_score = previous_score
        print("플레이 기록을 저장하지 못했습니다.")
        return False

    def show_score_records(self) -> None:
        """최고 점수와 최근 플레이 기록을 함께 출력한다."""
        self.show_section("최고 점수와 기록")
        score_text = (
            "기록 없음"
            if self.best_score is None
            else f"{self.best_score}점"
        )
        print(f"최고 점수: {score_text}")

        print(self.DETAIL_LINE)
        print("최근 플레이 기록")
        if not self.score_history:
            print("플레이 기록이 없습니다.")
            return

        recent_history = self.score_history[-5:]
        recent_history.reverse()
        for number, record in enumerate(recent_history, start=1):
            print(
                f"{number}. {record['played_at']}  {record['score']}점"
            )

    def safe_exit(self, interrupted: bool = False) -> None:
        """정상 종료와 입력 중단 종료의 안내를 한곳에서 처리한다."""
        self.save_state()
        if interrupted:
            print("")
            print("입력이 중단되었습니다.")
        print("게임을 종료합니다.")

    def run(self) -> None:
        """종료 메뉴를 선택할 때까지 메인 메뉴를 반복 실행한다."""
        try:
            while True:
                self.show_menu()
                choice = self.read_int("메뉴 선택(1~6): ", 1, 6)

                if choice == 6:
                    self.safe_exit()
                    return

                if choice == 1:
                    self.play_quizzes()
                elif choice == 2:
                    self.list_quizzes()
                elif choice == 3:
                    self.show_score_records()
                elif choice == 4:
                    self.add_quiz()
                elif choice == 5:
                    self.delete_quiz()
        # 모든 메뉴 기능에서 발생한 입력 중단을 함께 처리한다.
        except (KeyboardInterrupt, EOFError):
            self.safe_exit(interrupted=True)
