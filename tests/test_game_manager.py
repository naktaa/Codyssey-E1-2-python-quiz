import unittest

from src.game_manager import QuizGame
from src.quiz import Quiz


class InputFeeder:
    """준비된 값을 순서대로 반환해 테스트에서 키보드 입력을 대신한다."""

    def __init__(self, values: list[str]) -> None:
        self._values = iter(values)

    def __call__(self, prompt: str) -> str:
        return next(self._values)


class GameManagerMenuTest(unittest.TestCase):
    def make_game_manager(
        self,
        inputs: list[str],
        quizzes: list[Quiz] | None = None,
    ) -> tuple[QuizGame, list[str]]:
        """입력과 출력을 관찰할 수 있는 게임 관리자를 만든다."""
        outputs: list[str] = []
        game_manager = QuizGame(
            quizzes=quizzes,
            input_func=InputFeeder(inputs),
            output_func=outputs.append,
        )
        return game_manager, outputs

    def make_quiz(
        self,
        category: str,
        question: str,
        answer: int,
    ) -> Quiz:
        """플레이 흐름을 검증할 간단한 퀴즈를 만든다."""
        return Quiz(
            category=category,
            question=question,
            choices=["A", "B", "C", "D"],
            answer=answer,
        )

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
        game_manager, outputs = self.make_game_manager(["3", "5"])

        game_manager.run()

        self.assertEqual(outputs.count("=== 상식 퀴즈 게임 ==="), 2)
        self.assertIn("[퀴즈 목록 보기] 기능은 아직 구현되지 않았습니다.", outputs)
        self.assertEqual(outputs[-1], "게임을 종료합니다.")

    def test_get_categories_removes_duplicates_and_preserves_order(self) -> None:
        quizzes = [
            self.make_quiz("과학", "과학 문제 1", 1),
            self.make_quiz("역사", "역사 문제", 2),
            self.make_quiz("과학", "과학 문제 2", 3),
        ]
        game_manager, _ = self.make_game_manager([], quizzes)

        self.assertEqual(game_manager.get_categories(), ["과학", "역사"])

    def test_play_quizzes_handles_empty_quiz_list(self) -> None:
        game_manager, outputs = self.make_game_manager([])

        score = game_manager.play_quizzes()

        self.assertIsNone(score)
        self.assertEqual(outputs, ["등록된 퀴즈가 없습니다."])

    def test_play_quizzes_uses_selected_category_in_saved_order(self) -> None:
        quizzes = [
            self.make_quiz("과학", "첫 번째 과학 문제", 2),
            self.make_quiz("역사", "출제되면 안 되는 역사 문제", 1),
            self.make_quiz("과학", "두 번째 과학 문제", 4),
        ]
        game_manager, outputs = self.make_game_manager(
            ["1", "2", "3"],
            quizzes,
        )

        score = game_manager.play_quizzes()

        output_text = "\n".join(outputs)
        self.assertEqual(score, 50)
        self.assertLess(
            output_text.index("첫 번째 과학 문제"),
            output_text.index("두 번째 과학 문제"),
        )
        self.assertNotIn("출제되면 안 되는 역사 문제", output_text)
        self.assertIn("정답입니다!", outputs)
        self.assertIn("오답입니다. 정답은 4번 D입니다.", outputs)
        self.assertIn("정답 수: 1/2", outputs)
        self.assertIn("점수: 50점", outputs)
        self.assertEqual(game_manager.best_scores, {})

    def test_add_quiz_validates_input_and_adds_to_memory(self) -> None:
        inputs = [
            "   ",
            "문화",
            "",
            "대한민국의 수도는 어디인가요?",
            "",
            "서울",
            "부산",
            "인천",
            "대전",
            "abc",
            "5",
            "1",
        ]
        game_manager, outputs = self.make_game_manager(inputs)

        game_manager.add_quiz()

        self.assertEqual(len(game_manager.quizzes), 1)
        added_quiz = game_manager.quizzes[0]
        self.assertEqual(added_quiz.category, "문화")
        self.assertEqual(added_quiz.question, "대한민국의 수도는 어디인가요?")
        self.assertEqual(added_quiz.choices, ["서울", "부산", "인천", "대전"])
        self.assertEqual(added_quiz.answer, 1)
        self.assertIn("입력값이 비어 있습니다. 내용을 입력해 주세요.", outputs)
        self.assertIn("숫자만 입력해 주세요.", outputs)
        self.assertIn("1부터 4 사이의 숫자를 입력해 주세요.", outputs)
        self.assertEqual(outputs[-1], "퀴즈를 추가했습니다.")

    def test_add_quiz_uses_typed_existing_category_name(self) -> None:
        quizzes = [self.make_quiz("과학", "기존 문제", 1)]
        inputs = ["과학", "새 문제", "A", "B", "C", "D", "2"]
        game_manager, _ = self.make_game_manager(inputs, quizzes)

        game_manager.add_quiz()

        self.assertEqual(len(game_manager.quizzes), 2)
        self.assertEqual(game_manager.quizzes[-1].category, "과학")


if __name__ == "__main__":
    unittest.main()
