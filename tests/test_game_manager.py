import unittest

from src.game_manager import QuizGame


class InputFeeder:
    """준비된 값을 순서대로 반환해 테스트에서 키보드 입력을 대신한다."""

    def __init__(self, values: list[str]) -> None:
        self._values = iter(values)

    def __call__(self, prompt: str) -> str:
        return next(self._values)


class GameManagerMenuTest(unittest.TestCase):
    def make_game_manager(self, inputs: list[str]) -> tuple[QuizGame, list[str]]:
        """입력과 출력을 관찰할 수 있는 게임 관리자를 만든다."""
        outputs: list[str] = []
        game_manager = QuizGame(
            input_func=InputFeeder(inputs),
            output_func=outputs.append,
        )
        return game_manager, outputs

    def test_show_menu_displays_all_items(self) -> None:
        game_manager, outputs = self.make_game_manager([])

        game_manager.show_menu()

        self.assertIn("=== 상식 퀴즈 게임 ===", outputs)
        for number, label in game_manager.MENU_ITEMS.items():
            self.assertIn(f"{number}. {label}", outputs)

    def test_read_int_retries_invalid_values_and_strips_spaces(self) -> None:
        game_manager, outputs = self.make_game_manager(["", "abc", "9", "  3  "])

        result = game_manager.read_int("선택: ", 1, 5)

        self.assertEqual(result, 3)
        self.assertIn("입력값이 비어 있습니다. 숫자를 입력해 주세요.", outputs)
        self.assertIn("숫자만 입력해 주세요.", outputs)
        self.assertIn("1부터 5 사이의 숫자를 입력해 주세요.", outputs)

    def test_read_nonempty_retries_blank_values_and_strips_spaces(self) -> None:
        game_manager, outputs = self.make_game_manager(["   ", "  과학  "])

        result = game_manager.read_nonempty("카테고리: ")

        self.assertEqual(result, "과학")
        self.assertEqual(
            outputs,
            ["입력값이 비어 있습니다. 내용을 입력해 주세요."],
        )

    def test_run_returns_to_menu_for_placeholder_and_exits(self) -> None:
        game_manager, outputs = self.make_game_manager(["1", "5"])

        game_manager.run()

        self.assertEqual(outputs.count("=== 상식 퀴즈 게임 ==="), 2)
        self.assertIn("[퀴즈 풀기] 기능은 아직 구현되지 않았습니다.", outputs)
        self.assertEqual(outputs[-1], "게임을 종료합니다.")


if __name__ == "__main__":
    unittest.main()
