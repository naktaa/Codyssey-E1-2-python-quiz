import json
import shutil
from datetime import datetime
from pathlib import Path

from .default_quizzes import get_default_quizzes
from .quiz import Quiz


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE_PATH = PROJECT_ROOT / "state.json"
TEST_STATE_PATH = PROJECT_ROOT / "state.test.json"
ScoreRecord = dict[str, str | int]


class StateManager:
    """퀴즈 게임 상태의 JSON 저장, 검증, 복구를 전담한다."""

    def __init__(self, state_path: Path) -> None:
        self.state_path = state_path
        self.backup_path = state_path.with_name(f"{state_path.name}.bak")
        self._save_enabled = True

    def _create_default_state(
        self,
    ) -> tuple[
        list[Quiz],
        int | None,
        list[ScoreRecord],
    ]:
        """필요한 시점에 기본 퀴즈와 비어 있는 점수 기록을 만든다."""
        return get_default_quizzes(), None, []

    def save_state(
        self,
        quizzes: list[Quiz],
        best_score: int | None,
        score_history: list[ScoreRecord],
    ) -> bool:
        """이전 정상 상태를 백업하고 새 상태를 임시 파일로 교체한다."""
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
                json.dump(state_data, file, ensure_ascii=False, indent=4)
                file.write("\n")
            if not self.backup_valid_state():
                temp_path.unlink(missing_ok=True)
                return False
            temp_path.replace(self.state_path)
        except OSError as error:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass
            error_message = error.strerror or "알 수 없는 파일 오류"
            print(f"상태 파일을 저장하지 못했습니다: {error_message}")
            return False

        return True

    def load_valid_state_file(
        self,
        path: Path,
    ) -> tuple[
        list[Quiz],
        int | None,
        list[ScoreRecord],
    ]:
        """지정한 JSON 파일을 읽고 전체 상태 스키마를 검증한다."""
        with path.open("r", encoding="utf-8") as file:
            state_data = json.load(file)
        return self.validate_state_data(state_data)

    def backup_valid_state(self) -> bool:
        """교체 전 활성 파일이 정상이면 한 세대 복구 백업으로 보관한다."""
        if not self.state_path.exists():
            return True

        try:
            self.load_valid_state_file(self.state_path)
        except (json.JSONDecodeError, UnicodeError, TypeError, ValueError):
            # 손상된 활성 파일로 마지막 정상 백업을 덮어쓰지 않는다.
            return True
        except OSError as error:
            error_message = error.strerror or "알 수 없는 파일 오류"
            print(f"기존 상태 파일을 확인하지 못했습니다: {error_message}")
            print("이전 상태를 보호하기 위해 새 상태를 저장하지 않았습니다.")
            return False

        backup_temp_path = self.backup_path.with_name(
            f"{self.backup_path.name}.tmp"
        )
        try:
            shutil.copy2(self.state_path, backup_temp_path)
            backup_temp_path.replace(self.backup_path)
        except OSError as error:
            try:
                backup_temp_path.unlink(missing_ok=True)
            except OSError:
                pass
            error_message = error.strerror or "알 수 없는 파일 오류"
            print(f"정상 상태 백업을 만들지 못했습니다: {error_message}")
            print("이전 상태를 보호하기 위해 새 상태를 저장하지 않았습니다.")
            return False

        return True

    def validate_state_data(
        self,
        state: object,
    ) -> tuple[
        list[Quiz],
        int | None,
        list[ScoreRecord],
    ]:
        """JSON 구조를 검증해 게임에서 사용할 값으로 변환한다."""
        if not isinstance(state, dict):
            raise ValueError("상태 데이터는 객체 형식이어야 합니다.")

        quizzes_data = state.get("quizzes")
        score_history_data = state.get("score_history")
        if not isinstance(quizzes_data, list):
            raise ValueError("quizzes는 목록이어야 합니다.")
        if not isinstance(score_history_data, list):
            raise ValueError("score_history는 목록이어야 합니다.")

        loaded_quizzes = [Quiz.from_dict(data) for data in quizzes_data]
        loaded_score = state.get("best_score")
        if "best_score" not in state or (
            loaded_score is not None
            and (type(loaded_score) is not int or loaded_score < 0)
        ):
            raise ValueError("best_score는 null 또는 0 이상의 정수여야 합니다.")

        loaded_history = [
            self.validate_score_history(record)
            for record in score_history_data
        ]
        return loaded_quizzes, loaded_score, loaded_history

    def validate_score_history(
        self,
        record: object,
    ) -> ScoreRecord:
        """플레이 기록 한 건의 시각과 점수를 검증한다."""
        if not isinstance(record, dict):
            raise ValueError("플레이 기록은 객체여야 합니다.")

        played_at = record.get("played_at")
        if not isinstance(played_at, str):
            raise ValueError("플레이 기록 시간은 문자열이어야 합니다.")
        score = record.get("score")
        if type(score) is not int or score < 0:
            raise ValueError("플레이 기록의 점수는 0 이상의 정수여야 합니다.")

        return {
            "played_at": played_at,
            "score": score,
        }

    def backup_corrupted_state(self) -> Path | None:
        """손상된 상태 파일을 timestamp가 붙은 이름으로 복사한다."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = self.state_path.with_name(
            f"{self.state_path.name}.corrupt-{timestamp}"
        )
        collision_number = 1
        while backup_path.exists():
            backup_path = self.state_path.with_name(
                f"{self.state_path.name}.corrupt-{timestamp}-{collision_number}"
            )
            collision_number += 1
        try:
            shutil.copy2(self.state_path, backup_path)
        except OSError as error:
            error_message = error.strerror or "알 수 없는 파일 오류"
            print(f"손상된 상태 파일을 백업하지 못했습니다: {error_message}")
            return None
        return backup_path

    def load_recovery_backup(
        self,
    ) -> tuple[
        list[Quiz],
        int | None,
        list[ScoreRecord],
    ] | None:
        """마지막 정상 백업을 검증해 반환하고 사용할 수 없으면 안내한다."""
        try:
            return self.load_valid_state_file(self.backup_path)
        except FileNotFoundError:
            print("사용할 수 있는 마지막 정상 백업이 없습니다.")
        except OSError as error:
            error_message = error.strerror or "알 수 없는 파일 오류"
            print(f"마지막 정상 백업을 불러오지 못했습니다: {error_message}")
        except (json.JSONDecodeError, UnicodeError, TypeError, ValueError) as error:
            print(f"마지막 정상 백업도 손상되었습니다: {error}")
        return None

    def recover_corrupted_state(
        self,
    ) -> tuple[
        list[Quiz],
        int | None,
        list[ScoreRecord],
    ]:
        """손상 원본을 보존하고 마지막 정상 백업이나 기본 상태를 복구한다."""
        backup_path = self.backup_corrupted_state()

        if backup_path is None:
            self._save_enabled = False
            recovered_state = self.load_recovery_backup()
            if recovered_state is not None:
                print("마지막 정상 백업 데이터로 실행합니다.")
                print("손상 원본 보호를 위해 이번 실행에서는 저장하지 않습니다.")
                return recovered_state

            print("원본 보호를 위해 이번 실행에서는 상태를 저장하지 않습니다.")
            return self._create_default_state()

        print(f"손상된 상태 파일을 백업했습니다: {backup_path.name}")
        recovered_state = self.load_recovery_backup()
        if recovered_state is not None:
            if self.save_state(*recovered_state):
                print(f"마지막 정상 백업으로 복구했습니다: {self.backup_path.name}")
            else:
                self._save_enabled = False
                print("백업 데이터로 실행하지만 상태 파일은 복구하지 못했습니다.")
            return recovered_state

        default_state = self._create_default_state()
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
        list[ScoreRecord],
    ]:
        """상태 파일을 읽어 검증하고 없거나 손상된 경우 안전하게 복구한다."""
        if not self.state_path.exists():
            default_state = self._create_default_state()
            self.save_state(*default_state)
            return default_state

        try:
            loaded_quizzes, loaded_score, loaded_history = (
                self.load_valid_state_file(self.state_path)
            )
        except OSError as error:
            self._save_enabled = False
            error_message = error.strerror or "알 수 없는 파일 오류"
            print(f"상태 파일을 불러오지 못했습니다: {error_message}")
            print("원본 보호를 위해 이번 실행에서는 상태를 저장하지 않습니다.")
            return self._create_default_state()
        except (json.JSONDecodeError, UnicodeError, TypeError, ValueError) as error:
            print(f"상태 파일이 손상되었습니다: {error}")
            return self.recover_corrupted_state()

        return loaded_quizzes, loaded_score, loaded_history
