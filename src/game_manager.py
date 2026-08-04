from collections.abc import Callable

from .quiz import Quiz


class QuizGame:
    """터미널 퀴즈 게임의 메뉴와 공통 입력을 관리한다."""

    MENU_ITEMS = {
        1: "퀴즈 풀기",
        2: "퀴즈 추가",
        3: "퀴즈 목록 보기",
        4: "카테고리별 최고 점수",
        5: "종료",
    }

    def __init__(
        self,
        quizzes: list[Quiz] | None = None,
        input_func: Callable[[str], str] = input,
        output_func: Callable[[str], None] = print,
    ) -> None:
        # 전달받은 목록을 복사해 게임 밖의 목록 변경과 상태를 분리한다.
        self.quizzes = list(quizzes) if quizzes is not None else []
        self.best_scores: dict[str, int] = {}

        # 같은 게임 로직을 실제 터미널과 자동 테스트에서 함께 사용한다.
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
        """플레이할 카테고리를 번호로 선택하고 퀴즈가 없으면 None을 반환한다."""
        categories = self.get_categories()
        if not categories:
            self.output("등록된 퀴즈가 없습니다.")
            return None

        self.output("\n=== 카테고리 선택 ===")
        for number, category in enumerate(categories, start=1):
            self.output(f"{number}. {category}")

        choice = self.read_int("카테고리를 선택하세요: ", 1, len(categories))
        return categories[choice - 1]

    def play_quizzes(self) -> int | None:
        """선택한 카테고리의 퀴즈를 순서대로 출제하고 점수를 반환한다."""
        category = self.select_category()
        if category is None:
            return None

        selected_quizzes = [
            quiz
            for quiz in self.quizzes
            if quiz.category.casefold() == category.casefold()
        ]
        correct_count = 0

        self.output(f"\n=== {category} 퀴즈 ===")
        for number, quiz in enumerate(selected_quizzes, start=1):
            self.output("")
            quiz.display(output_func=self.output, number=number)
            user_answer = self.read_int("정답 번호를 입력하세요: ", 1, 4)

            if quiz.is_correct(user_answer):
                correct_count += 1
                self.output("정답입니다!")
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                self.output(
                    f"오답입니다. 정답은 {quiz.answer}번 {correct_choice}입니다."
                )

        total_count = len(selected_quizzes)
        score = round(correct_count / total_count * 100)
        self.output("\n=== 퀴즈 결과 ===")
        self.output(f"정답 수: {correct_count}/{total_count}")
        self.output(f"점수: {score}점")
        return score

    def run(self) -> None:
        """종료 메뉴를 선택할 때까지 메인 메뉴를 반복 실행한다."""
        while True:
            self.show_menu()
            choice = self.read_int("메뉴를 선택하세요: ", 1, 5)

            if choice == 5:
                self.output("게임을 종료합니다.")
                return

            if choice == 1:
                self.play_quizzes()
            else:
                self.output(
                    f"[{self.MENU_ITEMS[choice]}] 기능은 아직 구현되지 않았습니다."
                )
