from .quiz import Quiz


def get_default_quizzes() -> list[Quiz]:
    """상식 퀴즈의 기본 문제 목록을 새 객체로 반환한다."""
    return [
        Quiz(
            category="과학",
            question="물의 화학식은 무엇인가요?",
            choices=["CO2", "H2O", "O2", "NaCl"],
            answer=2,
        ),
        Quiz(
            category="과학",
            question="지구의 자연 위성은 무엇인가요?",
            choices=["태양", "화성", "달", "금성"],
            answer=3,
        ),
        Quiz(
            category="역사",
            question="훈민정음을 창제한 왕은 누구인가요?",
            choices=["세종", "태조", "영조", "정조"],
            answer=1,
        ),
        Quiz(
            category="역사",
            question="조선을 건국한 인물은 누구인가요?",
            choices=["이순신", "이성계", "강감찬", "장영실"],
            answer=2,
        ),
        Quiz(
            category="과학",
            question="태양계에서 가장 큰 행성은 무엇인가요?",
            choices=["지구", "화성", "목성", "금성"],
            answer=3,
        ),
    ]
