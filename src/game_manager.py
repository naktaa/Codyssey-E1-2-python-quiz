from collections.abc import Callable


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
        input_func: Callable[[str], str] = input,
        output_func: Callable[[str], None] = print,
    ) -> None:
        self.quizzes: list[object] = []
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

    def run(self) -> None:
        """종료 메뉴를 선택할 때까지 메인 메뉴를 반복 실행한다."""
        while True:
            self.show_menu()
            choice = self.read_int("메뉴를 선택하세요: ", 1, 5)

            if choice == 5:
                self.output("게임을 종료합니다.")
                return

            self.output(f"[{self.MENU_ITEMS[choice]}] 기능은 아직 구현되지 않았습니다.")
