from .quiz import Quiz


def get_default_quizzes() -> list[Quiz]:
    """직접 플레이를 확인할 임시 기본 퀴즈의 새 목록을 반환한다."""
    # 최종 제출 전 사용자가 준비한 상식 퀴즈 5개 이상으로 교체한다.
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
    ]
