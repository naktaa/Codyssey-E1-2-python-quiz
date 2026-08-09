from dataclasses import dataclass


@dataclass
class Quiz:
    """4지선다형 상식 문제와 문제별 힌트를 표현한다."""

    question: str
    choices: list[str]
    answer: int
    hint: str

    def __post_init__(self) -> None:
        """객체 생성 시 문자열을 정리하고 퀴즈 형식을 검증한다."""
        self.question = self._normalize_text(self.question, "문제")

        if not isinstance(self.choices, list) or len(self.choices) != 4:
            raise ValueError("선택지는 정확히 4개여야 합니다.")

        # 새 목록을 만들어 호출자가 전달한 원본 목록의 변경 영향을 막는다.
        self.choices = [
            self._normalize_text(choice, f"선택지 {index}")
            for index, choice in enumerate(self.choices, start=1)
        ]

        if type(self.answer) is not int or not 1 <= self.answer <= 4:
            raise ValueError("정답 번호는 1부터 4 사이의 정수여야 합니다.")

        self.hint = self._normalize_text(self.hint, "힌트")

    @staticmethod
    def _normalize_text(value: object, field_name: str) -> str:
        """필수 문자열의 공백을 정리하고 빈 값을 거부한다."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name}은(는) 비어 있을 수 없습니다.")
        return value.strip()

    def display(self, number: int | None = None) -> None:
        """문제와 번호가 붙은 선택지 4개를 출력한다."""
        prefix = f"{number}. " if number is not None else ""
        print(f"{prefix}{self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}) {choice}")

    def is_correct(self, user_answer: int) -> bool:
        """사용자가 선택한 번호가 정답인지 반환한다."""
        return user_answer == self.answer

    def to_dict(self) -> dict[str, object]:
        """JSON에 저장할 수 있는 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices.copy(),
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data: object) -> "Quiz":
        """딕셔너리를 검증해 Quiz 객체로 복원한다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터는 딕셔너리여야 합니다.")

        required_fields = ("question", "choices", "answer", "hint")
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            missing = ", ".join(missing_fields)
            raise ValueError(f"퀴즈 데이터에 필수 항목이 없습니다: {missing}")

        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data["hint"],
        )
