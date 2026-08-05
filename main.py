from src.default_quizzes import get_default_quizzes
from src.game_manager import QuizGame


def main() -> None:
    """게임 관리자를 생성해 터미널 퀴즈 게임을 시작한다."""
    game_manager = QuizGame(quizzes=get_default_quizzes())
    game_manager.load_state()
    game_manager.run()


if __name__ == "__main__":
    main()
