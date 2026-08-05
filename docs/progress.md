# 진행 상태

## 현재 단계

- 단계: 보너스 수동 힌트와 누적 점수 구현 완료
- 현재 통합 브랜치: `main`
- 현재 보너스 작업 브랜치: `feature/bonus`
- JSON 병합: `4984e31 Merge: JSON 상태 관리 브랜치 병합`
- 이번 보너스 브랜치 생성·첫 커밋 이후 Git 직접 조작은 사용자가 수행

## 검증 정책

- 2026-08-05 이후 `unittest`는 일절 실행하거나 수정하지 않는다.
- 기존 `tests/`는 과거 개발 과정의 기록으로만 유지한다.
- 과거의 17개 unittest 통과 기록은 당시 코드에 대한 이력이며 현재 JSON 코드의
  검증 결과로 사용하지 않는다.
- 이후 검증은 사용자가 `main.py`를 직접 실행해 제공한 원본 로그와 캡처로 남긴다.
- 문서 정합성 확인에는 코드 읽기, Git 상태 확인, `git diff --check` 같은
  비실행 검사를 사용할 수 있다.

## 구현 완료

### 프로그램 구조와 입력

- `Quiz`, `QuizGame` 클래스를 분리했다.
- 메뉴 1~5와 공통 정수 입력·비어 있지 않은 문자열 입력을 구현했다.
- 공백, 빈 입력, 문자, 범위 밖 숫자를 안내하고 다시 입력받는다.
- 정상 종료, Ctrl+C와 EOF를 `safe_exit()`에서 처리한다.

### 퀴즈 기능

- 퀴즈 데이터의 카테고리·문제·선택지 4개·정답 번호를 검증한다.
- 퀴즈의 출력, 정답 확인, JSON 딕셔너리 변환·복원을 메서드로 분리했다.
- 데이터에 처음 등장한 순서로 카테고리를 생성하고 하나를 선택해 플레이한다.
- 선택한 카테고리의 전체 문제 수 안에서 풀 개수를 선택한다.
- 선택한 개수만큼 중복 없이 무작위로 선택하고 반환된 순서대로 출제한다.
- 원본 퀴즈 객체 목록과 JSON 저장 순서는 변경하지 않는다.
- 문제마다 수동 힌트 사용 여부를 선택한다.
- 힌트는 정답과 무작위 오답 하나를 두 개의 후보로 표시한다.
- 힌트 없이 정답이면 3점, 힌트 사용 후 정답이면 1점, 오답이면 0점을 더한다.
- 결과에 정답 수, 힌트 사용 횟수와 `획득 점수/출제 문제 수 × 3점`을 출력한다.
- 새 카테고리를 포함해 퀴즈를 자유롭게 추가할 수 있다.
- 목록은 카테고리 제목 뒤 바로 문제를 표시하고, 각 문제 오른쪽에 구분자 없이
  선택지 4개를 나열하며 문제 사이를 한 줄 띄운다.
- 카테고리별 최고 점수를 비교해 더 높은 점수만 갱신하고, 미플레이 카테고리는
  `기록 없음`으로 표시한다.

### JSON 저장·불러오기

- 프로젝트 루트를 기준으로 상태 파일 경로를 계산한다.
- `save_state()`가 퀴즈와 최고 점수를 UTF-8, 한글 유지, 들여쓰기 2칸 JSON으로
  임시 파일에 쓴 뒤 활성 상태 파일로 교체한다.
- 퀴즈 추가 직후, 최고 점수 갱신 직후, 정상·중단 종료 시 저장한다.
- `load_state()`가 시작 시 JSON을 불러와 `Quiz` 목록과 최고 점수로 복원한다.
- 상태 파일이 없으면 기본 퀴즈와 빈 최고 점수로 새 파일을 만든다.
- 실제 게임은 `state.json`, 직접 기능 확인은 `QUIZ_STATE_MODE=test` 환경 변수로
  `state.test.json`을 사용한다.
- `state.test.json`, 손상 백업과 임시 파일은 Git에서 제외한다.

### 손상 파일 보호와 복구

- `validate_state_data()`가 최상위 객체, `quizzes` 목록, `best_scores` 객체와
  각 퀴즈·점수 값의 형식을 검증한다.
- JSON 문법·인코딩·스키마 오류는 원인 메시지를 출력한다.
- `backup_corrupted_state()`가 손상 원본을 timestamp가 붙은 이름으로 복사한다.
- 백업 성공 후 `recover_corrupted_state()`가 기본 퀴즈와 빈 점수로 활성 파일을
  복구한다.
- 백업에 실패하면 원본을 보호하도록 해당 실행의 저장을 비활성화한다.
- 저장은 임시 파일을 먼저 사용하고 실패 시 남은 임시 파일을 정리한다.

## 데이터 영속성 상태 구분

### 1. JSON 적용 전 메모리 동작 — 확인 완료

- 추가한 문제가 같은 실행에는 존재하지만 종료 후 사라지는 것을 사용자 직접
  실행으로 확인했다.
- 증거: [`../evidence/logs/memory-persistence-test.md`](../evidence/logs/memory-persistence-test.md)
- 이 로그는 현재 동작의 증거가 아니라 JSON 적용 전 비교 기준이다.

### 2. JSON 최고 점수 영속성 — 직접 재실행 확인 완료

- 퀴즈와 점수의 저장·불러오기 코드는 연결되어 있다.
- 테스트 데이터가 실제 `state.json`에 섞이지 않도록 실행 모드도 분리했다.
- 사용자가 확인용 파일에서 플레이 전 과학 `기록 없음`을 확인했다.
- 과학 문제 2개를 모두 맞혀 100점을 만든 뒤 정상 종료했다.
- 같은 명령으로 재실행해 과학 최고 점수 `100점`이 복원되는 것을 확인했다.
- 원본 로그: [`../evidence/logs/persistence-restart.md`](../evidence/logs/persistence-restart.md)
- `state.test.json`에는 `"과학": 100`이 남았고 실제 `state.json`의 Git diff는 없었다.

### 3. 추가 퀴즈 영속성 — 코드 구현 완료, 직접 재실행 미검증

- `add_quiz()`는 추가 직후 활성 상태 파일을 저장하도록 연결되어 있다.
- 이번 사용자 로그에는 새 퀴즈 추가와 재실행 후 목록 확인이 포함되지 않았다.
- 퀴즈 추가·종료·재실행·목록 확인 원본 로그가 추가로 필요하다.

### 4. JSON 손상 복구 — 직접 실행과 증거 확보 완료

- 사용자가 `QUIZ_STATE_MODE=test py`로 직접 실행했다.
- `quizzes`를 `quizes`로 잘못 적은 확인용 JSON에서
  `quizzes는 목록이어야 합니다.`를 확인했다.
- 화면에 표시된 백업 파일은
  `state.test.json.corrupt-20260805-181939-287895`이다.
- 해당 백업은 잘못된 `quizes` 키를 포함한 손상 원본을 그대로 보존하고,
  활성 `state.test.json`은 기본 문제 4개와 빈 최고 점수로 복구됐다.
- 증거: [복구 연결 기록](../evidence/logs/json-recovery.md),
  [터미널 캡처](../evidence/screenshots/json-recovery.png)

## Git 작업 기록

- 초기 저장소 설정과 `main` push 완료
- `feature/solving`에서 퀴즈 플레이를 구현하고 `cb4f9cb`에서 `main` 병합 완료
- 퀴즈 추가, 안전 종료, 목록, 최고 점수 기능을 `main`에서 기능별 커밋
- `state-json`에서 JSON 기능 3개 커밋과 문서 정리 커밋 완료 및 원격 동기화
  - `45990d1 Feat: state.json 저장과 불러오기 구현`
  - `40fdea5 Feat: 실행 모드별 상태 파일 분리`
  - `103a3b1 Fix: 손상된 상태 파일 백업과 복구 처리`
  - `02b454a Docs: JSON 구현과 검증 기록 정리`
- 최종 Git 그래프와 clone·pull 증거는 모든 기능과 `main` 병합이 끝난 뒤 정리

## 확보한 증거

- 초기 Git 설정: `evidence/git/git-verification.md`, `evidence/git/git-log.png`
- 초기 메뉴 화면: `evidence/screenshots/menu-test.png` — 개발 과정 자료
- 과거 브랜치 병합: `evidence/screenshots/git-merge.png` — 개발 과정 자료
- 메모리 동작 비교: `evidence/logs/memory-persistence-test.md`
- 안전 종료: `evidence/logs/safe-exit.md`, `evidence/screenshots/safe-exit.png`
- 퀴즈 목록: `evidence/screenshots/quiz-list.png`
- 최고 점수: `evidence/logs/best-score.md`
- 최고 점수 재실행 유지: `evidence/logs/persistence-restart.md`
- JSON 복구: `evidence/logs/json-recovery.md`, `evidence/screenshots/json-recovery.png`

## 최종 정리 시 확인할 항목

- 추가 퀴즈 영속성은 코드 구현과 점수 영속성 증거로 현재 개발을 진행하고,
  동료평가 또는 최종 직접 실행에서 다시 확인
- JSON 저장 중 실제 읽기·쓰기 OS 오류 직접 재현
- 빈 퀴즈 상태의 플레이·목록·점수 화면 최종 직접 확인
- 추가, 플레이 결과, 정상 영속성 재실행 화면·원본 로그
- 모든 기능 완료 후 메뉴와 Git 그래프 최종 증거
- 별도 디렉터리 clone·push와 기존 폴더 pull 반영 증거
- README 절차 기준 macOS zsh 최종 재현 로그

## 다음 권장 작업 하나

퀴즈 삭제 기능을 구현한다.

- 삭제할 카테고리와 문제 번호를 선택한다.
- 삭제할 문제를 보여주고 사용자 확인을 받은 뒤 목록에서 제거한다.
- 제거 직후 활성 상태 파일에 저장하고 재실행 후 삭제 유지 여부를 확인한다.
