# 요구사항 추적표

## 상태 기준

- `예정`: 아직 작업하지 않음
- `구현 중`: 현재 수정 중
- `구현 완료`: 코드 또는 문서 작성 완료
- `부분 검증`: 요구사항의 일부 동작만 직접 확인
- `실행 검증 완료`: 실제 명령으로 정상 동작 확인
- `증거 확보 완료`: 로그 또는 스크린샷 확보
- `문서 반영 완료`: README와 관련 문서에 최종 반영

코드를 작성했더라도 실행, 증거, 문서 반영이 끝나지 않았다면 최종 완료로 처리하지 않는다.

## 필수 요구사항

| ID | 요구사항 | 필수 여부 | 구현 위치 | 검증 방법 | 필요한 증거 | 구현 단계 | 권장 커밋 | 현재 상태 |
|---|---|---|---|---|---|---:|---|---|
| ENV-01 | Python 3.10 이상 사용 | 필수 | 개발 환경 | `python3 --version` | 환경 스크린샷 | 1 | `Chore: 프로젝트 초기 파일 구성` | 문서 반영 완료 |
| ENV-02 | 외부 라이브러리 없이 표준 라이브러리만 사용 | 필수 | 전체 코드 | import 목록과 직접 실행 확인 | 최종 검증 로그 | 13 | `Docs: 직접 실행 검증 결과 기록` | 구현 완료 |
| ENV-03 | macOS zsh에서 최종 재현 | 필수 | 전체 프로젝트 | README 절차로 새 터미널 실행 | 최종 검증 로그 | 16 | `Docs: macOS 최종 재현 기록` | 예정 |
| GIT-01 | GitHub 새 저장소와 로컬 저장소 설정 | 필수 | Git 저장소 | `git remote -v`, GitHub 확인 | 환경 또는 저장소 화면 | 1 | `Chore: 프로젝트 초기 파일 구성` | 문서 반영 완료 |
| GIT-02 | `.gitignore`, `README.md` 생성 후 첫 commit·push | 필수 | 루트 문서 | `git log -1`, 원격 저장소 | Git 로그 | 1 | `Chore: 프로젝트 초기 파일 구성` | 문서 반영 완료 |
| GIT-03 | 의미 있는 커밋 10개 이상 | 필수 | Git 이력 | `git rev-list --count HEAD` | Git 그래프 | 14 | 기능 단위 커밋 | 실행 검증 완료 |
| GIT-04 | main 외 브랜치 생성·작업·병합 1회 이상 | 필수 | `feature/solving` | `git log --graph --all` | Git 그래프 | 5~6 | `Feat: 퀴즈 출제와 결과 출력 구현` | 실행 검증 완료 |
| GIT-05 | `init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone` 각 1회 이상 사용 | 필수 | Git 작업 기록 | 터미널 기록·worklog 확인 | clone·pull 스크린샷 | 1, 5, 15 | 각 단계 커밋 | 구현 중 |
| FUNC-01 | 실행 시 메뉴와 종료 기능 제공 | 필수 | `src/game_manager.py` | 메뉴 1~6 선택 확인 | 메뉴 스크린샷 | 2 | `Feat: 메뉴와 공통 숫자 입력 처리 구현` | 구현 완료 |
| FUNC-02 | 메뉴 입력 공백·빈 값·문자·범위 오류 처리 | 필수 | 입력 메서드 | ` 1 `, Enter, `abc`, `9` 입력 | 메뉴 스크린샷·로그 | 2 | `Feat: 메뉴와 공통 숫자 입력 처리 구현` | 실행 검증 완료 |
| FUNC-03 | 숫자 입력이 필요한 모든 위치에 공통 검증 적용 | 필수 | 공통 입력 메서드 | 메뉴·정답·추가 정답 오류 직접 입력 | 최종 검증 로그 | 12 | `Fix: 공통 입력 예외 처리 보완` | 구현 완료 |
| FUNC-04 | Ctrl+C와 EOF에서 traceback 없이 안전 종료 | 필수 | 실행 루프·저장 메서드 | 입력 중 Ctrl+C, EOF 재현 | 최종 검증 로그 | 12 | `Fix: 입력 중단 시 안전 종료 처리` | 실행 검증 완료 |
| TECH-01 | `Quiz` 클래스 정의 | 필수 | `src/quiz.py` | 클래스 속성·인스턴스 확인 | 코드·실행 로그 | 3 | `Feat: Quiz 클래스 구현` | 실행 검증 완료 |
| TECH-02 | Quiz에 문제, 선택지 4개, 정답 속성 | 필수 | `src/quiz.py` | 객체 생성과 출력 확인 | 실행 로그 | 3 | `Feat: Quiz 클래스 구현` | 실행 검증 완료 |
| TECH-03 | Quiz 출력·정답 확인 등 메서드 분리 | 필수 | `src/quiz.py` | 플레이에서 메서드 호출 확인 | 실행 로그 | 3, 5 | `Feat: Quiz 클래스 구현` | 실행 검증 완료 |
| DATA-01 | 동일 주제의 직접 작성 기본 퀴즈 5개 이상 | 필수 | `src/default_quizzes.py`·`state.json` | 목록에서 개수·내용 확인 | 목록 스크린샷 | 4 | `Feat: 기본 퀴즈 데이터 추가` | 구현 완료 |
| FUNC-05 | 저장된 전체 상식 퀴즈 출제 | 필수 | `play_quizzes()` | 전체 목록에서 문제 수 선택과 무작위 출제 확인 | 플레이 스크린샷 | 5 | `Feat: 퀴즈 출제와 결과 출력 구현` | 실행 검증 완료 |
| FUNC-06 | 각 답 입력 후 정답·오답 안내 | 필수 | `src/game_manager.py` | 정답과 오답 각각 입력 | 플레이 스크린샷 | 5 | `Feat: 퀴즈 출제와 결과 출력 구현` | 실행 검증 완료 |
| FUNC-07 | 모든 문제 종료 후 정답 수·점수 결과 출력 | 필수 | `src/game_manager.py` | 플레이 완료 화면 | 플레이 스크린샷 | 5 | `Feat: 퀴즈 출제와 결과 출력 구현` | 실행 검증 완료 |
| FUNC-08 | 퀴즈가 없을 때 플레이 안내 후 메뉴 복귀 | 필수 | `src/game_manager.py` | 빈 목록 상태 직접 실행 | 최종 검증 로그 | 5 | `Feat: 퀴즈 출제와 결과 출력 구현` | 구현 완료 |
| FUNC-09 | 새 퀴즈의 문제·선택지 4개·정답·힌트 입력 | 필수 | `src/game_manager.py` | 카테고리 없이 새 퀴즈 등록 | 추가 스크린샷 | 7 | `Feat: 퀴즈 등록 기능 구현` | 실행 검증 완료 |
| FUNC-10 | 퀴즈 추가 입력 오류 처리 | 필수 | 입력 메서드 | 빈 문제·선택지, 잘못된 정답 직접 입력 | 최종 검증 로그 | 7, 12 | `Feat: 퀴즈 등록 기능 구현` | 구현 완료 |
| FUNC-11 | 추가 직후 저장하고 실패 시 메모리 추가 취소 | 필수 | `add_quiz()`·`save_state()` | 성공 시 JSON 반영, 실패 시 목록 원상 복구 확인 | 추가·JSON 증거 | 7, 11 | `Fix: 퀴즈 추가 저장 실패 처리 개선` | 부분 검증 |
| FUNC-12 | 저장된 퀴즈 목록 확인 | 필수 | `src/game_manager.py` | 메뉴에서 목록 출력 | 목록 스크린샷 | 8 | `Feat: 퀴즈 목록 조회 기능 구현` | 증거 확보 완료 |
| FUNC-13 | 퀴즈가 없을 때 목록 안내 | 필수 | `src/game_manager.py` | 빈 목록 상태 직접 실행 | 최종 검증 로그 | 8 | `Feat: 퀴즈 목록 조회 기능 구현` | 구현 완료 |
| FUNC-14 | 단일 최고 점수 조회 | 필수 | `src/game_manager.py` | 플레이 후 점수 메뉴 확인 | 점수 스크린샷 | 9 | `Feat: 최고 점수 계산과 조회 구현` | 실행 검증 완료 |
| FUNC-15 | 매 플레이 결과와 최고 점수 비교·갱신 | 필수 | `src/game_manager.py` | 낮은 점수·높은 점수 순서로 직접 확인 | 플레이·점수 증거 | 9 | `Feat: 최고 점수 계산과 조회 구현` | 실행 검증 완료 |
| FUNC-16 | 아직 플레이 전 상태 안내 | 필수 | `src/game_manager.py` | 초기 상태 점수 확인 | 최종 검증 로그 | 9 | `Feat: 최고 점수 계산과 조회 구현` | 증거 확보 완료 |
| TECH-04 | `QuizGame` 클래스 정의 | 필수 | `src/game_manager.py` | 인스턴스 생성과 실행 | 코드·실행 로그 | 10 | `Refactor: QuizGame 기능별 책임 정리` | 실행 검증 완료 |
| TECH-05 | 메뉴·플레이·추가·목록·점수·저장·불러오기 메서드 분리 | 필수 | `src/game_manager.py` | 코드 구조 검토 | 최종 코드 | 10 | `Refactor: QuizGame 기능별 책임 정리` | 구현 완료 |
| DATA-02 | 루트 `state.json`에 퀴즈와 단일 최고 점수 저장 | 필수 | `state.json`·`save_state()` | `best_score`와 카테고리 없는 퀴즈 확인 | persistence 스크린샷·로그 | 11 | `Feat: state.json 저장과 불러오기 구현` | 실행 검증 완료 |
| DATA-03 | UTF-8로 JSON 읽기·쓰기 | 필수 | `save_state()`·`load_state()` | 한글 퀴즈 저장 후 재실행 | persistence 증거 | 11 | `Feat: state.json 저장과 불러오기 구현` | 구현 완료 |
| DATA-04 | 파일이 없으면 기본 퀴즈 사용 | 필수 | `load_state()` | 확인용 상태 파일이 없는 첫 실행 | 최종 검증 로그 | 11 | `Feat: state.json 저장과 불러오기 구현` | 구현 완료 |
| DATA-05 | 손상 파일 안내 후 백업하고 기본 데이터로 정상 실행 | 필수 | `validate_state_data()`·복구 메서드 | 잘못된 확인용 JSON으로 직접 실행 | [복구 연결 기록](../evidence/logs/json-recovery.md) | 12 | `Fix: 손상된 상태 파일 백업과 복구 처리` | 증거 확보 완료 |
| DATA-06 | 읽기·쓰기 오류를 try/except로 처리 | 필수 | 저장·불러오기 메서드 | 코드 검토와 직접 오류 재현 | 최종 검증 로그 | 12 | `Fix: 데이터 입출력 예외 처리 보완` | 구현 완료 |
| DATA-07 | 종료·재실행 후 추가 퀴즈와 최고 점수 유지 | 필수 | 전체 프로그램 | 확인용 상태에서 추가·플레이·종료·재실행 | [재실행 원본 로그](../evidence/logs/persistence-restart.md)·추가 퀴즈 증거 | 13 | `Docs: 데이터 영속성 직접 검증 기록` | 부분 검증 |
| DOC-01 | README에 프로젝트 개요 포함 | 필수 | `README.md` | 항목 확인 | GitHub README | 14 | `Docs: README와 제출 증거 정리` | 구현 완료 |
| DOC-02 | README에 퀴즈 주제와 선정 이유 포함 | 필수 | `README.md` | 항목 확인 | GitHub README | 14 | `Docs: README와 제출 증거 정리` | 구현 완료 |
| DOC-03 | README에 실제·확인용 실행 방법 포함 | 필수 | `README.md` | 그대로 따라 직접 실행 | 최종 검증 로그 | 14, 16 | `Docs: README와 제출 증거 정리` | 구현 완료 |
| DOC-04 | README에 기능 목록·파일 구조 포함 | 필수 | `README.md` | 실제 코드와 비교 | GitHub README | 14 | `Docs: README와 제출 증거 정리` | 구현 완료 |
| DOC-05 | README에 실제·확인용 상태 경로, 역할·스키마·복구 포함 | 필수 | `README.md` | 실제 JSON·코드와 비교 | GitHub README | 14 | `Docs: README와 제출 증거 정리` | 구현 완료 |
| EVID-01 | 개발 환경 설정 화면 확보 | 필수 | `evidence/git/` | Python·Git·VSCode 표시 | `git-log.png` | 1 | `Docs: README와 제출 증거 정리` | 구현 중 |
| EVID-02 | 최종 메뉴·추가·목록·플레이·삭제·점수 기록 화면 확보 | 필수 | `evidence/screenshots/` | 각 기능 실제 실행 | 기능별 PNG | 13 | `Docs: README와 제출 증거 정리` | 구현 중 |
| EVID-03 | 재실행 데이터 유지 증거 확보 | 필수 | `evidence/logs/`·`evidence/screenshots/` | 종료 전후 비교 | 점수 원본 로그·추가 퀴즈 화면 | 13 | `Docs: README와 제출 증거 정리` | 구현 중 |
| EVID-04 | `git log --oneline --graph` 결과 확보 | 필수 | `evidence/screenshots/` | 브랜치·병합·커밋 수 확인 | `git-graph.png` | 16 | `Docs: README와 제출 증거 정리` | 구현 중 |
| EVID-05 | clone·push·pull 반영 증거 확보 | 필수 | `evidence/screenshots/`·worklog | 별도 폴더 실습 | `clone-pull.png` | 15 | `Docs: clone 실습 확인 문구 추가` | 예정 |
| SEC-01 | 저장소·로그·스크린샷에 비밀값 없음 | 필수 | 전체 제출물 | 토큰·키·인증정보 점검 | 최종 체크 결과 | 16 | `Docs: 제출 전 비밀값 점검 기록` | 예정 |

## 보너스 요구사항

보너스는 필수 기능 구현 후 사용자 승인에 따라 `feature/bonus`에서 진행했고,
사용자가 `main` 병합을 완료했다. 최신 실행 증거는 최종 단계에서 확보한다.

| ID | 요구사항 | 필수 여부 | 구현 위치 | 검증 방법 | 필요한 증거 | 구현 단계 | 권장 커밋 | 현재 상태 |
|---|---|---|---|---|---|---:|---|---|
| BONUS-01 | 문제 순서 랜덤 출제 | 선택 | `play_quizzes()`·`random.sample()` | 여러 번 직접 실행해 순서 변화 확인 | 실행 로그 | 선택 | `Feat: 퀴즈 랜덤 출제 추가` | 구현 완료 |
| BONUS-02 | 전체 상식 문제 중 풀이 수 선택 | 선택 | `select_quiz_count()`·`play_quizzes()` | 1~전체 범위 직접 확인 | 실행 로그 | 선택 | `Feat: 풀이 문제 수 선택 추가` | 실행 검증 완료 |
| BONUS-03 | 힌트와 점수 차감 | 선택 | `Quiz.hint`·`ask_for_hint()`·`show_hint()`·`play_quizzes()` | 문제별 저장 힌트와 사용 전후 누적 점수 확인 | 실행 로그 | 선택 | `Feat: 문제별 힌트 저장 방식 개선` | 실행 검증 완료 |
| BONUS-04 | 전체 목록에서 퀴즈 삭제 및 파일 반영 | 선택 | `read_yes_no()`·`delete_quiz()`·`save_state()` | 번호 선택, `y/n` 삭제·취소 후 재실행 | 실행 로그 | 선택 | `Feat: 퀴즈 삭제 기능 추가` | 실행 검증 완료 |
| BONUS-05 | 날짜·시간 포함 점수 기록 히스토리 | 선택 | `record_game_result()`·`show_score_history()`·JSON 스키마 | 6회 이상 플레이 후 최근 5개와 재실행 확인 | 실행 로그 | 선택 | `Feat: 점수 기록 히스토리 추가` | 구현 완료 |
