import json
import os
import random
import shutil
from collections.abc import Callable
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


class QuizGame:
    """터미널 퀴즈 게임의 메뉴와 공통 입력을 관리한다."""

    CORRECT_POINTS = 3
    HINT_CORRECT_POINTS = 1

    MENU_ITEMS = {
        1: "퀴즈 풀기",
        2: "퀴즈 목록 보기",
        3: "최고 점수와 기록",
        4: "퀴즈 추가",
        5: "퀴즈 삭제",
        6: "종료",
    }

    def __init__(
        self,
        quizzes: list[Quiz] | None = None,
        state_path: Path | None = None,
        input_func: Callable[[str], str] = input,
        output_func: Callable[[str], None] = print,
    ) -> None:
        # 전달받은 목록을 복사해 게임 밖의 목록 변경과 상태를 분리한다.
        self.quizzes = list(quizzes) if quizzes is not None else []
        self._default_quizzes = list(self.quizzes)
        self.best_scores: dict[str, int] = {}
        self.score_history: list[dict[str, str | int]] = []
        self.state_path = state_path or get_state_path()
        self._state_save_enabled = True

        # 입력과 출력을 주입할 수 있게 해 게임 흐름과 터미널을 분리한다.
        self.input = input_func
        self.output = output_func

    def show_menu(self) -> None:
        self.output("")
        self.output("=== 상식 퀴즈 게임 ===")
        for number, label in self.MENU_ITEMS.items():
            self.output(f"{number}. {label}")

    def read_int(self, prompt: str, minimum: int, maximum: int) -> int:
        """지정된 범위의 정수가 입력될 때까지 다시 입력받는다."""
        while True:
            raw_value = self.input(prompt).strip()

            if not raw_value:
                self.output("입력값이 비어 있습니다. 숫자를 입력해 주세요.")
                continue

            try:
                value = int(raw_value)
            except ValueError:
                self.output("숫자만 입력해 주세요.")
                continue

            if minimum <= value <= maximum:
                return value

            self.output(f"{minimum}부터 {maximum} 사이의 숫자를 입력해 주세요.")

    def read_nonempty(self, prompt: str) -> str:
        """공백이 아닌 문자열이 입력될 때까지 다시 입력받는다."""
        while True:
            value = self.input(prompt).strip()
            if value:
                return value

            self.output("입력값이 비어 있습니다. 내용을 입력해 주세요.")

    def read_yes_no(self, prompt: str) -> bool:
        """y 또는 n이 입력될 때까지 다시 입력받는다."""
        while True:
            answer = self.input(prompt).strip().casefold()
            if answer == "y":
                return True
            if answer == "n":
                return False
            self.output("y 또는 n을 입력해 주세요.")

    def save_state(self) -> bool:
        """현재 퀴즈, 최고 점수와 플레이 기록을 JSON 파일에 저장한다."""
        if not self._state_save_enabled:
            self.output("원본 상태 파일을 보호하기 위해 저장하지 않았습니다.")
            return False

        state = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_scores": self.best_scores,
            "score_history": self.score_history,
        }
        temp_path = self.state_path.with_name(f"{self.state_path.name}.tmp")

        try:
            with temp_path.open("w", encoding="utf-8", newline="\n") as file:
                json.dump(state, file, ensure_ascii=False, indent=2)
                file.write("\n")
            temp_path.replace(self.state_path)
        except OSError as error:
            self.remove_temp_state(temp_path)
            error_message = error.strerror or "알 수 없는 파일 오류"
            self.output(f"상태 파일을 저장하지 못했습니다: {error_message}")
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
        dict[str, int],
        list[dict[str, str | int]],
    ]:
        """불러온 JSON 구조를 검증해 게임 상태로 변환한다."""
        if not isinstance(state, dict):
            raise ValueError("상태 데이터는 객체 형식이어야 합니다.")

        quizzes_data = state.get("quizzes")
        best_scores_data = state.get("best_scores")
        score_history_data = state.get("score_history", [])
        if not isinstance(quizzes_data, list):
            raise ValueError("quizzes는 목록이어야 합니다.")
        if not isinstance(best_scores_data, dict):
            raise ValueError("best_scores는 객체여야 합니다.")
        if not isinstance(score_history_data, list):
            raise ValueError("score_history는 목록이어야 합니다.")

        loaded_quizzes = [Quiz.from_dict(data) for data in quizzes_data]
        loaded_scores: dict[str, int] = {}
        for category, score in best_scores_data.items():
            if not isinstance(category, str) or not category.strip():
                raise ValueError("최고 점수의 카테고리 이름이 올바르지 않습니다.")
            if isinstance(score, bool) or not isinstance(score, int):
                raise ValueError("최고 점수는 정수여야 합니다.")
            if score < 0:
                raise ValueError("최고 점수는 0 이상이어야 합니다.")
            loaded_scores[category.strip()] = score

        loaded_history = [
            self.validate_score_history(record)
            for record in score_history_data
        ]
        return loaded_quizzes, loaded_scores, loaded_history

    def validate_score_history(
        self,
        record: object,
    ) -> dict[str, str | int]:
        """플레이 기록 한 건의 필드와 값 범위를 검증한다."""
        if not isinstance(record, dict):
            raise ValueError("플레이 기록은 객체여야 합니다.")

        played_at = record.get("played_at")
        category = record.get("category")
        if not isinstance(played_at, str):
            raise ValueError("플레이 기록 시간은 문자열이어야 합니다.")
        try:
            datetime.strptime(played_at, "%Y-%m-%d %H:%M")
        except ValueError as error:
            raise ValueError(
                "플레이 기록 시간은 YYYY-MM-DD HH:MM 형식이어야 합니다."
            ) from error
        if not isinstance(category, str) or not category.strip():
            raise ValueError("플레이 기록의 카테고리가 올바르지 않습니다.")

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
            "category": category.strip(),
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
            self.output(f"손상된 상태 파일을 백업하지 못했습니다: {error_message}")
            return None
        return backup_path

    def recover_corrupted_state(self) -> bool:
        """손상 원본을 백업하고 기본 상태 파일을 만든다."""
        backup_path = self.backup_corrupted_state()
        if backup_path is None:
            self._state_save_enabled = False
            self.output("원본 보호를 위해 이번 실행에서는 상태를 저장하지 않습니다.")
            return False

        self.quizzes = list(self._default_quizzes)
        self.best_scores = {}
        self.score_history = []
        self.output(f"손상된 상태 파일을 백업했습니다: {backup_path.name}")

        if self.save_state():
            self.output("기본 데이터로 상태 파일을 복구했습니다.")
            return True

        self.output("기본 데이터로 실행하지만 상태 파일은 복구하지 못했습니다.")
        return False

    def load_state(self) -> bool:
        """상태 파일이 있으면 퀴즈와 최고 점수를 복원한다."""
        if not self.state_path.exists():
            return self.save_state()

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                state = json.load(file)
            loaded_quizzes, loaded_scores, loaded_history = (
                self.validate_state_data(state)
            )
        except OSError as error:
            self._state_save_enabled = False
            error_message = error.strerror or "알 수 없는 파일 오류"
            self.output(f"상태 파일을 불러오지 못했습니다: {error_message}")
            self.output("원본 보호를 위해 이번 실행에서는 상태를 저장하지 않습니다.")
            return False
        except (json.JSONDecodeError, UnicodeError, TypeError, ValueError) as error:
            self.output(f"상태 파일이 손상되었습니다: {error}")
            return self.recover_corrupted_state()

        self.quizzes = loaded_quizzes
        self.best_scores = loaded_scores
        self.score_history = loaded_history
        return True

    def add_quiz(self) -> None:
        """새 4지선다형 퀴즈를 입력받아 현재 게임의 목록에 추가한다."""
        self.output("\n=== 퀴즈 추가 ===")
        # 같은 이름은 기존 카테고리로, 새 이름은 새 카테고리로 사용한다.
        category = self.read_nonempty("카테고리 이름: ")
        question = self.read_nonempty("문제: ")
        choices = [
            self.read_nonempty(f"선택지 {number}: ")
            for number in range(1, 5)
        ]
        answer = self.read_int("정답 번호(1~4): ", 1, 4)

        new_quiz = Quiz(
            category=category,
            question=question,
            choices=choices,
            answer=answer,
        )
        self.quizzes.append(new_quiz)

        if self.save_state():
            self.output("퀴즈를 추가하고 저장했습니다.")
        else:
            self.output("퀴즈는 추가했지만 파일에는 저장하지 못했습니다.")

    def list_quizzes(self) -> None:
        """퀴즈 질문을 카테고리별로 묶어 연속해서 출력한다."""
        if not self.quizzes:
            self.output("등록된 퀴즈가 없습니다.")
            return

        self.output("\n=== 퀴즈 목록 ===")
        for category in self.get_categories():
            self.output(f"[{category}]")
            category_quizzes = [
                quiz
                for quiz in self.quizzes
                if quiz.category.casefold() == category.casefold()
            ]

            for number, quiz in enumerate(category_quizzes, start=1):
                self.output(f"{number}. {quiz.question}")

    def delete_quiz(self) -> bool:
        """선택한 퀴즈를 확인 후 삭제하고 상태 파일에 저장한다."""
        if not self.quizzes:
            self.output("등록된 퀴즈가 없습니다.")
            return False

        self.output("\n=== 퀴즈 삭제 ===")
        category = self.select_category()
        if category is None:
            return False

        category_quizzes = [
            quiz
            for quiz in self.quizzes
            if quiz.category.casefold() == category.casefold()
        ]
        self.output("\n=== 삭제할 문제 선택 ===")
        for number, quiz in enumerate(category_quizzes, start=1):
            self.output(f"{number}. {quiz.question}")

        choice = self.read_int(
            "삭제할 문제 번호를 입력하세요: ",
            1,
            len(category_quizzes),
        )
        selected_quiz = category_quizzes[choice - 1]
        self.output(f"삭제할 문제: {selected_quiz.question}")
        if not self.read_yes_no("정말 삭제하시겠습니까? (y/n): "):
            self.output("퀴즈 삭제를 취소했습니다.")
            return False

        quiz_index = next(
            index
            for index, quiz in enumerate(self.quizzes)
            if quiz is selected_quiz
        )
        previous_scores = self.best_scores.copy()
        self.quizzes.pop(quiz_index)

        category_exists = any(
            quiz.category.casefold() == category.casefold()
            for quiz in self.quizzes
        )
        if not category_exists:
            self.best_scores = {
                score_category: score
                for score_category, score in self.best_scores.items()
                if score_category.casefold() != category.casefold()
            }

        if self.save_state():
            self.output("퀴즈를 삭제하고 저장했습니다.")
            return True

        self.quizzes.insert(quiz_index, selected_quiz)
        self.best_scores = previous_scores
        self.output("파일에 저장하지 못해 퀴즈 삭제를 취소했습니다.")
        return False

    def get_categories(self) -> list[str]:
        """퀴즈에 처음 등장한 순서대로 중복 없는 카테고리를 반환한다."""
        categories: list[str] = []
        seen: set[str] = set()

        for quiz in self.quizzes:
            category_key = quiz.category.casefold()
            if category_key not in seen:
                seen.add(category_key)
                categories.append(quiz.category)

        return categories

    def select_category(self) -> str | None:
        """카테고리를 번호로 선택하고 퀴즈가 없으면 None을 반환한다."""
        categories = self.get_categories()
        if not categories:
            self.output("등록된 퀴즈가 없습니다.")
            return None

        self.output("\n=== 카테고리 선택 ===")
        for number, category in enumerate(categories, start=1):
            self.output(f"{number}. {category}")

        choice = self.read_int("카테고리를 선택하세요: ", 1, len(categories))
        return categories[choice - 1]

    def select_quiz_count(self, category: str, total_count: int) -> int:
        """선택한 카테고리에서 풀 문제 수를 입력받는다."""
        self.output(f"\n{category} 카테고리에는 총 {total_count}문제가 있습니다.")
        return self.read_int(
            f"풀 문제 수를 입력하세요(1~{total_count}): ",
            1,
            total_count,
        )

    def show_hint(self, quiz: Quiz) -> None:
        """정답과 오답 하나를 남긴 두 개의 정답 후보를 출력한다."""
        wrong_numbers = [
            number
            for number in range(1, len(quiz.choices) + 1)
            if number != quiz.answer
        ]
        hint_numbers = sorted([quiz.answer, random.choice(wrong_numbers)])
        hint_choices = " 또는 ".join(
            f"{number}) {quiz.choices[number - 1]}"
            for number in hint_numbers
        )
        self.output(f"힌트: 정답 후보는 {hint_choices} 중 하나입니다.")

    def ask_for_hint(self, quiz: Quiz) -> bool:
        """힌트 사용 여부를 입력받고 사용 여부를 반환한다."""
        self.output("힌트를 사용하시겠습니까?")
        self.output("1. 힌트 보기")
        self.output("2. 바로 풀기")
        choice = self.read_int("선택하세요: ", 1, 2)
        if choice == 1:
            self.show_hint(quiz)
            return True
        return False

    def play_quizzes(self) -> int | None:
        """선택한 카테고리에서 지정한 수의 퀴즈를 출제한다."""
        category = self.select_category()
        if category is None:
            return None

        selected_quizzes = [
            quiz
            for quiz in self.quizzes
            if quiz.category.casefold() == category.casefold()
        ]
        quiz_count = self.select_quiz_count(category, len(selected_quizzes))
        # 원본 저장 순서는 유지하고 이번 플레이의 출제 목록만 무작위로 만든다.
        selected_quizzes = random.sample(selected_quizzes, k=quiz_count)
        correct_count = 0
        hint_count = 0
        score = 0

        self.output(f"\n=== {category} 퀴즈 ===")
        for number, quiz in enumerate(selected_quizzes, start=1):
            self.output("")
            quiz.display(output_func=self.output, number=number)
            hint_used = self.ask_for_hint(quiz)
            if hint_used:
                hint_count += 1
            user_answer = self.read_int("정답 번호를 입력하세요: ", 1, 4)

            if quiz.is_correct(user_answer):
                correct_count += 1
                earned_points = (
                    self.HINT_CORRECT_POINTS
                    if hint_used
                    else self.CORRECT_POINTS
                )
                score += earned_points
                self.output(f"정답입니다! {earned_points}점을 획득했습니다.")
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                self.output(
                    f"오답입니다. 정답은 {quiz.answer}번 {correct_choice}입니다."
                )

        total_count = len(selected_quizzes)
        max_score = total_count * self.CORRECT_POINTS
        self.output("\n=== 퀴즈 결과 ===")
        self.output(f"정답 수: {correct_count}/{total_count}")
        self.output(f"힌트 사용: {hint_count}회")
        self.output(f"점수: {score}점")
        if self.record_game_result(
            category=category,
            score=score,
            max_score=max_score,
            correct_count=correct_count,
            total_count=total_count,
            hint_count=hint_count,
        ):
            self.output(f"새로운 최고 점수: {score}점")
        return score

    def update_best_score(self, category: str, score: int) -> bool:
        """기존 기록보다 높은 카테고리 점수로 메모리 값을 갱신한다."""
        previous_score = self.best_scores.get(category)
        if previous_score is None or score > previous_score:
            self.best_scores[category] = score
            return True
        return False

    def record_game_result(
        self,
        category: str,
        score: int,
        max_score: int,
        correct_count: int,
        total_count: int,
        hint_count: int,
    ) -> bool:
        """완료한 플레이를 기록하고 최고 점수와 함께 한 번 저장한다."""
        previous_scores = self.best_scores.copy()
        is_new_best = self.update_best_score(category, score)
        record: dict[str, str | int] = {
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": category,
            "score": score,
            "max_score": max_score,
            "correct_count": correct_count,
            "total_count": total_count,
            "hint_count": hint_count,
        }
        self.score_history.append(record)

        if self.save_state():
            return is_new_best

        self.score_history.pop()
        self.best_scores = previous_scores
        self.output("플레이 기록을 저장하지 못했습니다.")
        return False

    def show_best_scores(self) -> None:
        """카테고리별 최고 점수 또는 기록 없음 상태를 출력한다."""
        categories = self.get_categories()
        if not categories:
            self.output("등록된 퀴즈가 없습니다.")
            return

        self.output("\n=== 카테고리별 최고 점수 ===")
        for category in categories:
            score = self.best_scores.get(category)
            score_text = "기록 없음" if score is None else f"{score}점"
            self.output(f"{category}: {score_text}")

    def show_score_history(self) -> None:
        """플레이 시각 기준 최근 기록을 최대 5개 출력한다."""
        self.output("\n=== 최근 플레이 기록 ===")
        if not self.score_history:
            self.output("플레이 기록이 없습니다.")
            return

        indexed_history = enumerate(self.score_history)
        recent_history = sorted(
            indexed_history,
            key=lambda item: (item[1]["played_at"], item[0]),
            reverse=True,
        )[:5]
        for number, (_, record) in enumerate(recent_history, start=1):
            self.output(
                f"{number}. {record['played_at']}  {record['category']}  "
                f"{record['score']}점  "
                f"정답 {record['correct_count']}/{record['total_count']}  "
                f"힌트 {record['hint_count']}회"
            )

    def show_score_records(self) -> None:
        """카테고리별 최고 점수와 최근 플레이 기록을 함께 출력한다."""
        self.show_best_scores()
        self.show_score_history()

    def safe_exit(self, interrupted: bool = False) -> None:
        """정상 종료와 입력 중단 종료의 안내를 한곳에서 처리한다."""
        self.save_state()
        if interrupted:
            self.output("")
            self.output("입력이 중단되었습니다.")
        self.output("게임을 종료합니다.")

    def run(self) -> None:
        """종료 메뉴를 선택할 때까지 메인 메뉴를 반복 실행한다."""
        try:
            while True:
                self.show_menu()
                choice = self.read_int("메뉴를 선택하세요: ", 1, 6)

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
