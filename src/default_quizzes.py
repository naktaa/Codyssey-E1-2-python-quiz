from .quiz import Quiz


def get_default_quizzes() -> list[Quiz]:
    """실제 기본 문제를 추가하기 전까지 새로운 빈 목록을 반환한다."""
    return []
