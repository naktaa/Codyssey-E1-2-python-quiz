import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from .quiz import Quiz


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE_PATH = PROJECT_ROOT / "state.json"
TEST_STATE_PATH = PROJECT_ROOT / "state.test.json"
STATE_MODE_ENV = "QUIZ_STATE_MODE"


def get_state_path() -> Path:
    """실행 모드에 맞는 실제 또는 테스트 상태 파일 경로를 반환한다."""
    state_mode = os.getenv(STATE_MODE_ENV, "real").strip().casefold()
    if state_mode == "real":
        return DEFAULT_STATE_PATH
    if state_mode == "test":
        return TEST_STATE_PATH
    raise ValueError(f"{STATE_MODE_ENV}는 real 또는 test여야 합니다.")


class StateManager:
    """퀴즈 게임 상태의 JSON 저장, 검증, 복구를 전담한다."""

    def __init__(self, state_path: Path, default_quizzes: list[Quiz]) -> None:
        self.state_path = state_path
        self._default_quizzes = list(default_quizzes)
        self._save_enabled = True

    def create_default_state(
        self,
    ) -> tuple[
        list[Quiz],
        int | None,
        list[dict[str, str | int]],
    ]:
        """기본 퀴즈와 비어 있는 점수 기록으로 새 상태를 만든다."""
        return list(self._default_quizzes), None, []

    def save_state(
        self,
        quizzes: list[Quiz],
        best_score: int | None,
        score_history: list[dict[str, str | int]],
    ) -> bool:
        """게임 상태를 임시 JSON 파일에 쓴 뒤 활성 파일로 교체한다."""
        if not self._save_enabled:
            print("원본 상태 파일을 보호하기 위해 저장하지 않았습니다.")
            return False

        state_data = {
            "quizzes": [quiz.to_dict() for quiz in quizzes],
            "best_score": best_score,
            "score_history": score_history,
        }
        temp_path = self.state_path.with_name(f"{self.state_path.name}.tmp")

        try:
            with temp_path.open("w", encoding="utf-8", newline="\n") as file:
                json.dump(state_data, file, ensure_ascii=False, indent=2)
                file.write("\n")
            temp_path.replace(self.state_path)
        except OSError as error:
            self.remove_temp_state(temp_path)
            error_message = error.strerror or "알 수 없는 파일 오류"
            print(f"상태 파일을 저장하지 못했습니다: {error_message}")
            return False

        return True

    def remove_temp_state(self, temp_path: Path) -> None:
        """저장 실패 후 남은 임시 상태 파일을 가능한 범위에서 정리한다."""
        try:
            temp_path.unlink(missing_ok=True)
        except OSError:
            pass

    def validate_state_data(
        self,
        state: object,
    ) -> tuple[
        list[Quiz],
        int | None,
        list[dict[str, str | int]],
    ]:
        """JSON 구조를 검증해 게임에서 사용할 값으로 변환한다."""
        if not isinstance(state, dict):
            raise ValueError("상태 데이터는 객체 형식이어야 합니다.")

        quizzes_data = state.get("quizzes")
        score_history_data = state.get("score_history", [])
        if not isinstance(quizzes_data, list):
            raise ValueError("quizzes는 목록이어야 합니다.")
        if not isinstance(score_history_data, list):
            raise ValueError("score_history는 목록이어야 합니다.")

        loaded_quizzes = [Quiz.from_dict(data) for data in quizzes_data]
        if "best_score" in state:
            loaded_score = state["best_score"]
            if loaded_score is not None and (
                isinstance(loaded_score, bool)
                or not isinstance(loaded_score, int)
                or loaded_score < 0
            ):
                raise ValueError("best_score는 null 또는 0 이상의 정수여야 합니다.")
        else:
            loaded_score = self.load_legacy_best_score(state)

        loaded_history = [
            self.validate_score_history(record)
            for record in score_history_data
        ]
        return loaded_quizzes, loaded_score, loaded_history

    def load_legacy_best_score(self, state: dict[object, object]) -> int | None:
        """기존 카테고리별 점수 중 최댓값을 단일 최고 점수로 이전한다."""
        legacy_scores = state.get("best_scores")
        if not isinstance(legacy_scores, dict):
            raise ValueError("best_score는 null 또는 0 이상의 정수여야 합니다.")

        scores: list[int] = []
        for category, score in legacy_scores.items():
            if not isinstance(category, str) or not category.strip():
                raise ValueError("기존 최고 점수의 카테고리가 올바르지 않습니다.")
            if (
                isinstance(score, bool)
                or not isinstance(score, int)
                or score < 0
            ):
                raise ValueError("기존 최고 점수는 0 이상의 정수여야 합니다.")
            scores.append(score)
        return max(scores, default=None)

    def validate_score_history(
        self,
        record: object,
    ) -> dict[str, str | int]:
        """플레이 기록 한 건의 필드와 값 범위를 검증한다."""
        if not isinstance(record, dict):
            raise ValueError("플레이 기록은 객체여야 합니다.")

        played_at = record.get("played_at")
        if not isinstance(played_at, str):
            raise ValueError("플레이 기록 시간은 문자열이어야 합니다.")
        try:
            datetime.strptime(played_at, "%Y-%m-%d %H:%M")
        except ValueError as error:
            raise ValueError(
                "플레이 기록 시간은 YYYY-MM-DD HH:MM 형식이어야 합니다."
            ) from error

        number_fields = {
            "score": record.get("score"),
            "max_score": record.get("max_score"),
            "correct_count": record.get("correct_count"),
            "total_count": record.get("total_count"),
            "hint_count": record.get("hint_count"),
        }
        for field_name, value in number_fields.items():
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"플레이 기록의 {field_name}은 정수여야 합니다.")

        score = number_fields["score"]
        max_score = number_fields["max_score"]
        correct_count = number_fields["correct_count"]
        total_count = number_fields["total_count"]
        hint_count = number_fields["hint_count"]
        if total_count < 1 or max_score < 1:
            raise ValueError("플레이 기록의 문제 수와 만점은 1 이상이어야 합니다.")
        if not 0 <= score <= max_score:
            raise ValueError("플레이 기록의 점수가 올바르지 않습니다.")
        if not 0 <= correct_count <= total_count:
            raise ValueError("플레이 기록의 정답 수가 올바르지 않습니다.")
        if not 0 <= hint_count <= total_count:
            raise ValueError("플레이 기록의 힌트 수가 올바르지 않습니다.")

        return {
            "played_at": played_at,
            "score": score,
            "max_score": max_score,
            "correct_count": correct_count,
            "total_count": total_count,
            "hint_count": hint_count,
        }

    def backup_corrupted_state(self) -> Path | None:
        """손상된 상태 파일을 timestamp가 붙은 이름으로 복사한다."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup_path = self.state_path.with_name(
            f"{self.state_path.name}.corrupt-{timestamp}"
        )
        try:
            shutil.copy2(self.state_path, backup_path)
        except OSError as error:
            error_message = error.strerror or "알 수 없는 파일 오류"
            print(f"손상된 상태 파일을 백업하지 못했습니다: {error_message}")
            return None
        return backup_path

    def recover_corrupted_state(
        self,
    ) -> tuple[
        list[Quiz],
        int | None,
        list[dict[str, str | int]],
    ]:
        """손상 원본을 백업하고 기본 상태 파일을 만든다."""
        default_state = self.create_default_state()
        backup_path = self.backup_corrupted_state()
        if backup_path is None:
            self._save_enabled = False
            print("원본 보호를 위해 이번 실행에서는 상태를 저장하지 않습니다.")
            return default_state

        print(f"손상된 상태 파일을 백업했습니다: {backup_path.name}")
        if self.save_state(*default_state):
            print("기본 데이터로 상태 파일을 복구했습니다.")
            return default_state

        print("기본 데이터로 실행하지만 상태 파일은 복구하지 못했습니다.")
        return default_state

    def load_state(
        self,
    ) -> tuple[
        list[Quiz],
        int | None,
        list[dict[str, str | int]],
    ]:
        """상태 파일을 읽어 검증하고 없거나 손상된 경우 안전하게 복구한다."""
        if not self.state_path.exists():
            default_state = self.create_default_state()
            self.save_state(*default_state)
            return default_state

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                state_data = json.load(file)
            loaded_quizzes, loaded_score, loaded_history = (
                self.validate_state_data(state_data)
            )
        except OSError as error:
            self._save_enabled = False
            error_message = error.strerror or "알 수 없는 파일 오류"
            print(f"상태 파일을 불러오지 못했습니다: {error_message}")
            print("원본 보호를 위해 이번 실행에서는 상태를 저장하지 않습니다.")
            return self.create_default_state()
        except (json.JSONDecodeError, UnicodeError, TypeError, ValueError) as error:
            print(f"상태 파일이 손상되었습니다: {error}")
            return self.recover_corrupted_state()

        self.restore_missing_default_hints(loaded_quizzes)
        return loaded_quizzes, loaded_score, loaded_history

    def restore_missing_default_hints(self, quizzes: list[Quiz]) -> None:
        """기존 JSON의 기본 문제에 누락된 힌트를 기본 데이터에서 보완한다."""
        default_hints = {
            quiz.question.casefold(): quiz.hint
            for quiz in self._default_quizzes
            if quiz.hint is not None
        }
        for quiz in quizzes:
            if quiz.hint is None:
                quiz.hint = default_hints.get(quiz.question.casefold())
