import argparse

from src.default_quizzes import get_default_quizzes
from src.game_manager import QuizGame
from src.state_manager import DEFAULT_STATE_PATH, TEST_STATE_PATH, StateManager


def main() -> None:
    """게임 관리자를 생성해 터미널 퀴즈 게임을 시작한다."""
    parser = argparse.ArgumentParser(description="터미널 상식 퀴즈 게임")
    parser.add_argument(
        "--test",
        action="store_true",
        help="실제 데이터 대신 state.test.json을 사용합니다.",
    )
    args = parser.parse_args()

    state_path = TEST_STATE_PATH if args.test else DEFAULT_STATE_PATH
    if args.test:
        print("[테스트 모드] state.test.json을 사용합니다.")

    default_quizzes = get_default_quizzes()
    state_manager = StateManager(
        state_path=state_path,
        default_quizzes=default_quizzes,
    )
    game_manager = QuizGame(state_manager)
    game_manager.load_state()
    game_manager.run()


if __name__ == "__main__":
    main()
