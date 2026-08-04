import unittest

from src.default_quizzes import get_default_quizzes
from src.quiz import Quiz


class QuizTest(unittest.TestCase):
    def make_quiz(self, **overrides: object) -> Quiz:
        """일부 값만 바꿔 검증할 수 있는 정상 퀴즈를 만든다."""
        data: dict[str, object] = {
            "category": "과학",
            "question": "물의 화학식은 무엇인가요?",
            "choices": ["CO2", "H2O", "O2", "NaCl"],
            "answer": 2,
        }
        data.update(overrides)
        return Quiz(**data)

    def test_create_quiz_strips_text_and_copies_choices(self) -> None:
        original_choices = [" CO2 ", " H2O ", " O2 ", " NaCl "]

        quiz = self.make_quiz(
            category=" 과학 ",
            question=" 물의 화학식은 무엇인가요? ",
            choices=original_choices,
        )
        original_choices[0] = "변경됨"

        self.assertEqual(quiz.category, "과학")
        self.assertEqual(quiz.question, "물의 화학식은 무엇인가요?")
        self.assertEqual(quiz.choices, ["CO2", "H2O", "O2", "NaCl"])

    def test_rejects_blank_category_and_question(self) -> None:
        for field in ("category", "question"):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    self.make_quiz(**{field: "   "})

    def test_rejects_invalid_choices(self) -> None:
        invalid_choices = [
            ["하나", "둘", "셋"],
            ["하나", "둘", "셋", "   "],
            "문자열은 선택지 목록이 아님",
        ]

        for choices in invalid_choices:
            with self.subTest(choices=choices):
                with self.assertRaises(ValueError):
                    self.make_quiz(choices=choices)

    def test_rejects_invalid_answer(self) -> None:
        for answer in (0, 5, "2", True):
            with self.subTest(answer=answer):
                with self.assertRaises(ValueError):
                    self.make_quiz(answer=answer)

    def test_display_and_answer_check(self) -> None:
        quiz = self.make_quiz()
        outputs: list[str] = []

        quiz.display(output_func=outputs.append, number=3)

        self.assertEqual(outputs[0], "3. 물의 화학식은 무엇인가요?")
        self.assertEqual(outputs[1], "  1) CO2")
        self.assertEqual(outputs[-1], "  4) NaCl")
        self.assertTrue(quiz.is_correct(2))
        self.assertFalse(quiz.is_correct(1))

    def test_dictionary_round_trip_uses_independent_choice_lists(self) -> None:
        original = self.make_quiz()

        data = original.to_dict()
        restored = Quiz.from_dict(data)
        data["choices"][0] = "변경됨"

        self.assertEqual(restored, original)
        self.assertEqual(restored.choices[0], "CO2")

    def test_from_dict_rejects_invalid_data(self) -> None:
        with self.assertRaises(ValueError):
            Quiz.from_dict([])

        with self.assertRaisesRegex(ValueError, "answer"):
            Quiz.from_dict(
                {
                    "category": "과학",
                    "question": "문제",
                    "choices": ["1", "2", "3", "4"],
                }
            )

    def test_default_quizzes_returns_fresh_empty_lists(self) -> None:
        first = get_default_quizzes()
        second = get_default_quizzes()

        self.assertEqual(first, [])
        self.assertEqual(second, [])
        self.assertIsNot(first, second)


if __name__ == "__main__":
    unittest.main()
