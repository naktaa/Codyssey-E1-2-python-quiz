from src.default_quizzes import get_default_quizzes
from src.game_manager import QuizGame
from src.state_manager import TEST_STATE_PATH, StateManager, get_state_path


def main() -> None:
    """게임 관리자를 생성해 터미널 퀴즈 게임을 시작한다."""
    state_path = get_state_path()
    if state_path == TEST_STATE_PATH:
        print("[테스트 모드] state.test.json을 사용합니다.")

    default_quizzes = get_default_quizzes()
    state_manager = StateManager(
        state_path=state_path,
        default_quizzes=default_quizzes,
    )
    game_manager = QuizGame(default_quizzes, state_manager=state_manager)
    game_manager.load_state()
    game_manager.run()


if __name__ == "__main__":
    main()
