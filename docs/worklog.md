# 작업 기록

실제 수행한 내용만 날짜별로 기록한다. 실행하지 않은 명령과 예상 결과는 기록하지 않는다.

## 현재 기록 원칙

- 기능 확인은 사용자가 `main.py`를 직접 실행한 결과를 기준으로 한다.
- 사용자가 제공한 콘솔 로그는 내용을 재구성하지 않고 원문 중심으로 보존한다.
- 구현, 직접 실행 확인, 증거 확보와 미검증 상태를 구분한다.
- 계정명·호스트명은 별도 마스킹 대상으로 보지 않으며 토큰·키·인증정보는 기록하지 않는다.

## 기록 형식

### YYYY-MM-DD — 작업 제목

- 환경: macOS / zsh / Python x.y.z
- 브랜치: `브랜치명`
- 목표: 이번 작업의 한 가지 목표
- 요구사항: `FUNC-xx`, `GIT-xx`

#### 변경 파일

- `파일명`: 실제 변경 내용

#### 실행 명령과 실제 결과

```zsh
실제로 실행한 명령
```

- 결과: 성공 또는 실패
- 실제 출력 요약: 확인한 사실만 기록

#### 증거

- `evidence/...`: 실제 생성한 파일만 기록

#### Git 상태

- 커밋: 실제 커밋 해시와 메시지 또는 `미커밋`
- push: 완료 / 미실시

#### 다음 작업

- 다음에 수행할 논리적 단계 하나

---

## 2026-08-09 — 보너스 기능을 유지한 코드 구조 단순화

- 환경: Linux / bash / Python 3.12.3
- 브랜치: `main`
- 기준 커밋: `13ec031 Docs: 리드미 변경 및 단순화`
- 목표: 최근 플레이 기록과 타이머를 유지하면서 이전 스키마 호환 코드와 불필요한
  간접 호출을 제거한다.

### 변경 내용

- 환경 변수 대신 `python3 main.py --test`로 테스트 상태 파일을 선택한다.
- 플레이 기록은 `played_at`과 `score`만 저장한다.
- 최근 기록은 저장된 마지막 5개를 역순으로 출력한다.
- 이전 `best_scores` 변환과 누락 힌트 복원 코드를 제거했다.
- `remove_temp_state()`, `select_quiz_count()`, `update_best_score()`, 개별 점수 출력
  메서드를 상위 흐름에 합쳤다.
- `QuizGame`은 이미 생성된 `StateManager`를 필수로 전달받는다.
- 퀴즈를 모두 삭제해도 완료한 플레이의 최고 점수와 기록은 유지한다.
- 임시 파일 교체, 손상 원본 백업, 저장 비활성화와 메모리 rollback은 유지한다.

### 실행 검증

```zsh
python3 main.py --help
printf '6\n' | python3 main.py --test
```

- Python 파일 7개의 구문 검사를 통과했다.
- `--help`에 `--test` 옵션이 표시됐다.
- 테스트 모드에서 `state.test.json`을 새로 만들고 메뉴 1~6과 정상 종료를 확인했다.
- 테스트 모드에서 퀴즈를 추가하고 목록에서 확인한 뒤 삭제해 기본 5문제 상태로
  돌아오는 것을 확인했다.
- `state.test.json`은 `.gitignore`에 의해 Git 변경사항에 포함되지 않았다.
- 임시 상태에 점수 6건을 저장하고 최근 5건이 최신순으로 표시되는 것을 확인했다.
- 최고 점수와 최근 기록의 재로드, 마지막 퀴즈 삭제 후 점수 유지, 저장 실패
  rollback을 확인했다.
- 이전 `best_scores`와 힌트가 누락된 퀴즈가 현재 스키마에서 거부되는 것을 확인했다.

---

## 2026-08-07 — README 정보 순서와 전체 게임 흐름 단순화

- 환경: Linux / bash / Python 3.12.3
- 브랜치: `main`
- 작업 시작 기준:
  `462a29c Refactor: 상태 관리 책임 분리 및 문서 구조 개선`
- 목표: 처음 읽는 사용자가 게임, 파일 구조와 전체 실행 흐름을 순서대로 빠르게
  이해할 수 있도록 README를 재구성한다.

### 변경 내용

- 게임 소개 직후 프로젝트 구조를 배치하고, 그다음 객체와 파일의 역할을 설명한다.
- 별도 점수 정책 절을 제거하고 힌트 전 3점, 힌트 후 1점, 오답·시간 초과 0점
  규칙을 게임 소개에 포함한다.
- 복잡한 메뉴·상태 분기 Mermaid를 실행→상태 복원→메뉴→기능→변경 시 저장
  →반복 또는 종료만 보여주는 단일 흐름으로 교체한다.
- 메뉴별 동작과 저장 여부는 다이어그램 대신 표로 구분한다.
- 동료평가 실행 순서를 문서 뒤쪽의 기능 확인 체크리스트로 변경한다.
- 상태 파일의 정상·없음·손상 처리는 데이터 저장 절의 짧은 목록으로 정리한다.

### 검증

- README 주요 절의 순서가 프로젝트 개요→구조→객체 역할→실행 방법→기능
  →전체 흐름→데이터 저장→평가 체크리스트 순서인지 확인했다.
- Mermaid 코드 블록이 하나만 존재하고 Markdown 코드 펜스가 닫혔는지 확인했다.
- README와 관련 문서의 로컬 링크가 모두 존재하는지 확인했다.
- `python3 -m py_compile main.py src/*.py`와 `git diff --check`를 통과했다.
- 게임 코드와 추적 중인 `state.json`은 변경하지 않았다.

### Git 상태

- 현재 README와 진행·작업 기록 변경: 미커밋
- push: 미실시

---

## 2026-08-07 — 상태 관리 책임 분리와 README 재구성

- 환경: Linux / bash / Python 3.12.3
- 브랜치: `main`
- 작업 시작 기준: `9485d5f Docs: 필요 산출물 및 진행 상태 갱신`
- 목표: 길어진 `QuizGame`에서 JSON 상태 책임을 분리하고, 현재 구현을 동료평가에서
  설명하기 쉬운 README 구조로 정리한다.

### 구조 변경

- `src/state_manager.py`를 추가했다.
- `StateManager`가 상태 경로, 기본 상태, JSON 저장·불러오기, 스키마 검증,
  이전 점수 처리, 누락 힌트 복원과 손상 파일 백업·복구를 담당한다.
- `QuizGame`은 메뉴와 게임 진행을 유지하고, 얇은 `save_state()`·`load_state()`로
  `StateManager`에 파일 처리를 위임한다.
- `main.py`가 기본 퀴즈와 상태 경로를 사용해 `StateManager`를 생성하고
  `QuizGame`에 전달하도록 변경했다.
- 처음 검토한 `GameState`와 `StateLoadResult`는 현재 규모에서 설명 단계를 늘린다고
  판단해 제거했다. 세 상태 값은 메서드 인자와 반환 튜플로 직접 전달한다.
- `QuizGame` 생성자의 `state_path`·`state_manager` 이중 선택도 제거하고,
  필요한 경우 `StateManager` 객체 하나만 전달하도록 단순화했다.
- `QuizGame`은 550줄에서 340줄로 줄었다.

### 확정한 점수 정책

- 최고 점수는 문제 수로 정규화하지 않고 실제 획득 점수만 비교한다.
- 더 많은 문제를 선택할수록 최대 획득 점수가 높아지는 동작을 유지한다.
- 점수 정규화는 남은 고려사항이 아니라 적용하지 않기로 확정한 정책이다.

### README와 관련 문서

- README를 프로젝트 개요, 필수·추가 기능, 동료평가 확인 순서, 객체 책임,
  점수 정책, 상태 스키마와 복구 중심으로 재작성했다.
- 메서드별 세부 구현, 긴 개발 배경과 개별 커밋 나열은 README에서 제거했다.
- `docs/architecture-plan.md`를 `StateManager` 합성 구조 기준으로 갱신했다.
- 요구사항 추적표의 JSON 구현 위치를 `src/state_manager.py`로 변경했다.
- 진행 문서를 `9485d5f` 이후 현재 작업 상태로 갱신했다.
- 과거 troubleshooting 기록은 유지하고 현재 상태 책임 위치만 덧붙였다.

### 실행 검증

실제 `state.json`을 변경하지 않도록 임시 디렉터리의 상태 파일로 검사했다.

```zsh
python3 -m py_compile main.py src/*.py
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
# 임시 상태 파일로 생성·추가·삭제·플레이·복구·롤백 검사
PY
```

확인 결과:

- 전체 Python 파일 구문과 import 성공
- `main.py`의 객체 조립, 정상 종료와 EOF 안전 종료 성공
- 파일 없음 → 기본 퀴즈 5개 저장 → 재로드 성공
- 퀴즈 추가·삭제 후 재로드 성공
- 플레이 후 최고 점수와 히스토리 재로드 성공
- 이전 카테고리별 점수 이전과 누락된 기본 힌트 복원 성공
- 손상 JSON 백업과 기본 상태 복구 성공
- 손상 파일 백업 실패 후 원본 유지와 이후 저장 차단 성공
- 저장 실패 시 퀴즈 추가 롤백 성공
- 저장 실패 시 퀴즈 삭제 롤백 성공
- 저장 실패 시 플레이 기록과 최고 점수 롤백 성공
- README와 관련 문서의 로컬 링크 확인 성공
- `git diff --check` 성공
- 추적 중인 `state.json` 변경 없음

### 남은 작업

- macOS에서 README 동료평가 순서로 최종 직접 실행한다.
- 추가 퀴즈와 점수의 재실행 유지 원본 증거를 확보한다.
- 최종 Git 그래프와 clone·push·pull 증거를 확보한다.
- commit: `462a29c Refactor: 상태 관리 책임 분리 및 문서 구조 개선`
- push: `origin/main`에 완료

---

## 초기 상태

- 초기 문서 템플릿만 준비된 상태에서 작업을 시작함
- 프로그램 코드 구현과 실행 검증은 아직 수행하지 않음

---

## 2026-08-01 — Git 저장소 초기화와 첫 push

- 환경: macOS / zsh / Python 3.12.13 / Git 2.53.0
- 브랜치: `main`
- 목표: 로컬 저장소를 초기화하고 초기 문서를 GitHub의 `main` 브랜치에 게시
- 요구사항: `ENV-01`, `GIT-01`, `GIT-02`, `GIT-05`, `EVID-01`

### 변경 파일

- 초기 커밋: `.gitattributes`, `.gitignore`, 미션·README·진행 문서와 증거 폴더 기본 구조
- `evidence/git/git-log.png`: Python·Git 버전과 첫 커밋 동기화 상태 화면
- `evidence/git/git-verification.md`: 초기화, 커밋, 원격 연결과 push 결과 기록
- `docs/requirements.md`: 실제 완료·진행 상태 반영
- `docs/progress.md`: 현재 단계와 다음 작업 갱신
- `README.md`: 초기 Git 설정 결과와 증거 링크 반영

### 실행 명령과 실제 결과

```zsh
git init -b main
git status --short --branch
git add .
git commit -m "Chore: 프로젝트 초기 파일 구성"
git remote add origin https://github.com/naktaa/Codyssey-E1-2-python-quiz.git
git push -u origin main
git log -1 --oneline --decorate
git status --short --branch
```

- 결과: 성공
- 실제 출력 요약: 첫 커밋 `a4887e4`를 생성하고 `origin/main`에 push했다.
- 실제 출력 요약: 로컬 `main`이 `origin/main`을 추적하며 같은 커밋을 가리키는 것을 확인했다.
- 확인 필요: Git이 커미터 이름과 이메일을 자동 추정했으므로 다음 커밋 전에 저장소 로컬 설정을 확인한다.

### 증거

- `evidence/git/git-verification.md`
- `evidence/git/git-log.png`

### Git 상태

- 커밋: `a4887e4 Chore: 프로젝트 초기 파일 구성`
- push: `origin/main`에 완료
- 현재 문서와 증거 변경: 미커밋

### 다음 작업

- 다음 커밋 전에 저장소 로컬 Git 사용자 이름과 이메일을 명시적으로 설정하고 값을 확인한다.

---

## 2026-08-04 — 상식 퀴즈 아키텍처와 구현 계획 정리

- 환경: macOS / zsh / Python 3.12.13 / Git 2.53.0
- 브랜치: `main`
- 목표: 확정된 상식 퀴즈 구조와 단계별 구현·커밋 계획을 별도 문서로 보존
- 요구사항: `DOC-01`, `DOC-02`, `DOC-04`, `GIT-03`, `GIT-04`

### 작업 시작 상태

- 작업 트리: 깨끗함
- 로컬 `main`과 `origin/main`: `51b89d6`에서 동기화
- 기존 커밋: 3개
- 저장소 로컬 Git 사용자 이름·이메일: 값 노출 없이 설정 유무 확인 완료

### 변경 파일

- `docs/architecture-plan.md`: 아키텍처, 데이터 스키마, 기능 흐름, 예외 처리,
  검증과 단계별 Git 계획 작성
- `README.md`: 주제와 카테고리별 점수 스키마를 확정하고 계획 문서 링크 추가
- `docs/progress.md`: 실제 Git 기준 상태, 확정된 설계와 다음 작업 반영
- `docs/worklog.md`: 이번 문서화 작업의 실제 내용 기록

### 실행 명령과 실제 결과

```zsh
git status --short --branch
git log --oneline --decorate -5
git config --local --get user.name
git config --local --get user.email
git diff --check
git status --short
```

- 결과: 성공
- 실제 출력 요약: 작업 시작 시 `main`과 `origin/main`이 `51b89d6`에서
  동기화되어 있고 작업 트리가 깨끗한 것을 확인했다.
- 실제 출력 요약: 기존 커밋 3개와 저장소 로컬 Git 사용자 설정 유무를
  확인했으며 문서에는 이름과 이메일 값을 기록하지 않았다.
- 실제 출력 요약: `git diff --check`가 출력 없이 통과했으며 변경 범위가
  계획 문서와 README·진행 문서로 제한된 것을 확인했다.

### 증거

- 새 증거 파일 없음

### Git 상태

- 커밋: `6960262 Docs: 상식 퀴즈 구현 계획 정리`
- push: 미실시

### 다음 작업

- 메뉴 1~5와 공통 입력 처리를 담당하는 최소 `QuizGame` 골격을 구현한다.

---

## 2026-08-04 — 메뉴와 공통 입력 처리 구현

- 환경: macOS / zsh / Python 3.12.13 / Git 2.53.0
- 브랜치: `main`
- 목표: `src` 소스 구조에서 메뉴 1~5와 이후 기능에 재사용할 입력 검증 구현
- 요구사항: `FUNC-01`, `FUNC-02`, `TECH-04`, `TECH-05`

### 변경 파일

- `main.py`: `src.game_manager`의 `QuizGame`을 실행하는 진입점 추가
- `src/__init__.py`: 애플리케이션 코드 패키지 정의
- `src/game_manager.py`: 메뉴 루프, 숫자 입력과 비어 있지 않은 문자열 입력 구현
- `README.md`: 메뉴와 공통 입력의 검증 상태 반영
- `docs/requirements.md`: 실제 구현·검증 상태 반영
- `docs/progress.md`: 현재 단계와 다음 작업 갱신
- `docs/troubleshooting.md`: 실제 테스트·컴파일 실패와 해결 기록

### 실행 명령과 실제 결과

```zsh
env PYTHONPYCACHEPREFIX=/private/tmp/codyssey-e1-2-pycache python3 -m compileall -q .
printf '1\n5\n' | python3 main.py
```

- 결과: 성공
- 실제 출력 요약: 임시 bytecode 캐시 경로를 사용한 전체 Python 컴파일이
  출력 없이 성공했다.
- 실제 출력 요약: 메뉴 1번 선택 시 미구현 안내 후 메뉴로 돌아오고 5번
  선택 시 traceback 없이 종료했다.

### 증거

- `evidence/screenshots/menu-test.png`: 메뉴·오류 입력·정상 종료 예비 화면
- 화면에 로컬 계정명과 호스트명이 표시되어 최종 제출용으로는 재촬영 필요

### Git 상태

- 커밋: `3b3914c Feat: 메뉴와 공통 입력 처리 구현`
- 주석 보완: `442d924 Docs: 게임 매니저 코드 설명 보완`
- 예비 화면: `8f954a2 Feat: 메뉴와 공통 입력 처리 구현`
- push: `origin/main`에 완료

### 다음 작업

- `Quiz` 클래스의 데이터 검증, 출력, 정답 확인과 JSON 변환을 구현한다.

---

## 2026-08-04 — Quiz 클래스와 빈 기본 데이터 구조 구현

- 환경: macOS / zsh / Python 3.12.13 사용자 확인
- 브랜치: `main`
- 목표: 퀴즈 한 문제의 형식과 JSON 변환 책임을 `Quiz` 클래스로 분리
- 요구사항: `TECH-01`, `TECH-02`, `TECH-03`, `DATA-01`

### 변경 파일

- `src/quiz.py`: 데이터 클래스, 생성 검증, 출력, 정답 확인과 딕셔너리 변환 구현
- `src/default_quizzes.py`: 실제 문제 반영 전 사용할 새로운 빈 목록 제공
- `src/game_manager.py`: 퀴즈 목록 타입을 `list[Quiz]`로 구체화
- `README.md`, `docs/architecture-plan.md`: 실행 명령을 Python 3.12.13의
  `python` 기준으로 정리

### 실행 명령과 실제 결과

```zsh
python --version
```

- 결과: 성공
- 실제 출력: `Python 3.12.13`

### 증거

- 새 스크린샷 없음

### Git 상태

- 커밋: `6e55f31 Feat: 퀴즈 클래스 기본 구현`
- push: `origin/main`에 완료

### 다음 작업

- `feature/solving` 브랜치를 생성한다.

---

## 2026-08-04 — feature/solving 브랜치와 카테고리별 퀴즈 플레이

- 환경: macOS / zsh / Python 3.12.13 사용자 환경
- 브랜치: `feature/solving`
- 목표: 선택한 카테고리의 문제를 순서대로 출제하고 결과 점수를 출력
- 요구사항: `GIT-04`, `GIT-05`, `DATA-01`, `FUNC-05`, `FUNC-06`, `FUNC-07`, `FUNC-08`

### 브랜치 생성 명령과 실제 결과

```zsh
git checkout -b feature/solving
git branch
```

- 결과: 성공
- 실제 출력 요약: 새 `feature/solving` 브랜치를 생성하고 해당 브랜치로
  전환했다.
- 실제 출력 요약: `git branch`에서 `feature/solving`이 현재 브랜치로
  표시되는 것을 다시 확인했다.

### 변경 파일

- `src/game_manager.py`: 카테고리 추출·선택, 순차 출제, 정오답과 결과 출력 구현
- `main.py`: 기본 퀴즈를 생성해 `QuizGame`에 전달하도록 연결
- `src/default_quizzes.py`: 과학·역사 플레이 확인용 임시 문제 4개 추가
- `README.md`: 플레이 구현 상태와 실제 기능 브랜치명 반영
- `docs/architecture-plan.md`: 브랜치 생성·병합 명령을 `feature/solving`으로 변경
- `docs/requirements.md`: 브랜치와 플레이 요구사항 구현 상태 반영
- `docs/progress.md`: 현재 브랜치, 구현 범위와 다음 검증 작업 반영

### 실행 명령과 실제 결과

```zsh
git diff --check
```

- 결과: 성공
- 실제 출력 요약: 공백 오류 없이 통과했다.

### 증거

- 브랜치 생성 터미널 로그를 작업 기록에 반영
- 실제 문제를 추가한 뒤 `evidence/screenshots/play-result.png` 확보 예정

### Git 상태

- 커밋: `65312c4 Feat: 퀴즈 풀기 기능 기본 구현`
- push: `origin/feature/solving`에 완료
- `main` 병합: `cb4f9cb Merge: 퀴즈 플레이 브랜치 병합`

### 다음 작업

- Python 3.12.13 환경에서 직접 플레이 흐름을 확인한다.

---

## 2026-08-04 — main 메모리 기반 퀴즈 추가 구현

- 환경: macOS / zsh / Python 3.12.13 사용자 환경
- 브랜치: `main`
- 목표: JSON 저장 없이 퀴즈 등록 입력과 같은 실행 내 사용을 먼저 검증
- 요구사항: `FUNC-09`, `FUNC-10`

### 변경 파일

- `src/game_manager.py`: 카테고리 이름, 문제, 선택지 4개와 정답을 입력해 메모리 목록에 추가
- `README.md`: 메모리 기반 퀴즈 추가 구현 상태 반영
- `docs/architecture-plan.md`: 등록 단계와 파일 저장 단계를 분리해 기록
- `docs/requirements.md`: 퀴즈 등록과 입력 오류 처리 구현 상태 반영
- `docs/progress.md`: 현재 브랜치와 다음 수동 검증 작업 반영

### 분리 상태

- `main`: JSON 관련 코드와 `state.json` 없이 퀴즈를 실행 중 메모리에만 추가
- `feature/state-json`: 기본 JSON 저장 구현 커밋 `b4cc983`을 원격에 보관

### 검증

- 사용자 터미널에서 `py main.py`로 직접 실행했다.
- 과학 카테고리에 `test` 문제와 선택지 4개를 입력해 추가했다.
- 정답 번호 `6`에 범위 오류가 출력되고 `1`을 다시 입력해 등록을 완료했다.
- 종료 후 재실행했을 때 기본 과학 문제 2개만 출제되어 추가 문제가
  메모리와 함께 사라지는 것을 확인했다.
- 같은 실행 내 추가 문제 플레이는 후속 상태 점검에서 확인했다.

### 증거

- `evidence/logs/memory-persistence-test.md`: 추가·범위 오류·재실행 소멸 실제 로그
- 추후 JSON 저장·불러오기 구현 후 같은 시나리오로 영속성 결과를 비교한다.

### Git 상태

- 커밋: `b78bcc1 Feat: 퀴즈 추가 기능 구현`
- push: `origin/main`에 완료

---

## 2026-08-04 — 현재 구현·문서 상태 점검

- 환경: macOS / zsh / Python 3.12.13 / Git 2.53.0
- 브랜치: `main`
- 목표: 오늘까지의 코드·실행·Git·증거 상태를 대조하고 진행 문서를 최신화
- 요구사항: `ENV-02`, `GIT-03`, `GIT-04`, `FUNC-03`, `FUNC-05`~`FUNC-10`, `TECH-01`~`TECH-04`

### 실행 명령과 실제 결과

```zsh
git status --short --branch
git rev-list --count HEAD
git log --oneline --graph --decorate --all -20
PYTHONPYCACHEPREFIX=/private/tmp/codyssey-e1-2-audit-pycache python -m compileall -q .
git diff --check
printf '2\n문화\n대한민국의 수도는?\n서울\n부산\n인천\n대전\n1\n1\n3\n1\n5\n' | python main.py
python main.py < /dev/null
```

- 전체 Python 파일 컴파일과 `git diff --check`가 출력 없이 통과했다.
- 새 문화 퀴즈를 추가한 뒤 같은 실행에서 해당 카테고리를 선택해 100점으로
  플레이하고 정상 종료했다.
- `main`의 커밋 수는 13개이고 `feature/solving` 병합 커밋의 두 부모와
  분기·병합 그래프를 확인했다.
- 표준 라이브러리 외 import가 없음을 확인했다.
- 빈 입력 스트림으로 실행하면 `EOFError` traceback과 종료 코드 1이 발생했다.
  안전 종료는 미해결 필수 요구사항으로 유지한다.

### 문서 변경

- `README.md`: 현재 기능·검증·Git·증거 상태와 실행 환경 주의사항 반영
- `docs/requirements.md`: 실제 구현·실행 검증 상태 반영
- `docs/progress.md`: 현재 Git 상태, 완료 작업, 다음 작업과 차단 요소 갱신
- `docs/worklog.md`: 완료된 커밋·병합·push와 상태 점검 결과 기록

### 증거

- 새 증거 파일 없음
- 기존 예비 PNG의 계정명·호스트명 노출을 최종 재촬영 대상으로 확인

### Git 상태

- 점검 시작 전: `main`과 로컬 `origin/main`이 `b78bcc1`에서 같고 작업 트리 깨끗함
- 현재 변경: 진행 기록 Markdown 파일만 수정
- commit·push: 사용자 요청이 없어 미실시
- 권장 커밋 메시지: `Docs: 현재 구현 및 검증 상태 갱신`

### 다음 작업

- 메뉴 3번의 퀴즈 목록 보기와 빈 목록 안내를 구현한다.

---

## 2026-08-05 — EOF와 Ctrl+C 입력 중단 안전 종료

- 환경: macOS / zsh / Python 3.12.13
- 브랜치: `main`
- 목표: 어느 입력 단계에서든 EOF와 Ctrl+C를 traceback 없이 처리
- 요구사항: `FUNC-04`, `TECH-05`

### 변경 파일

- `src/game_manager.py`: `safe_exit()` 추가, `run()` 전체 입력 중단 처리
- `evidence/logs/safe-exit.md`: 사용자 직접 실행 원문 기록
- `README.md`, `docs/requirements.md`, `docs/progress.md`: 검증 상태 반영
- `docs/troubleshooting.md`: 실제 EOF traceback과 해결 내용 기록

### 실행 명령과 실제 결과

```zsh
printf '5\n' | python main.py
python main.py < /dev/null
python main.py
# 입력 대기 중 Ctrl+C
git diff --check
```

- 결과: 성공
- 실제 출력 요약: 정상 종료, EOF와 Ctrl+C가 모두 종료 코드 0으로 끝났다.
- 실제 출력 요약: 입력 중단 시 안내 메시지가 출력되고 traceback은 없었다.

### 증거

- `evidence/logs/safe-exit.md`
- `evidence/screenshots/safe-exit.png`

### Git 상태

- 커밋: `49f97b5 Fix: 입력 중단 시 안전 종료 처리`
- push: `origin/main`에 완료

### 다음 작업

- 메뉴 3번의 퀴즈 목록 보기와 빈 목록 안내를 구현한다.

---

## 2026-08-05 — 카테고리별 퀴즈 목록 조회

- 환경: macOS / zsh / Python 3.12.13
- 브랜치: `main`
- 목표: 메뉴 3번에서 문제와 선택지를 읽기 쉬운 목록으로 확인
- 요구사항: `FUNC-12`, `FUNC-13`, `EVID-02`

### 변경 파일

- `src/game_manager.py`: `list_quizzes()` 추가와 메뉴 3번 연결
- `evidence/screenshots/quiz-list.png`: 사용자 직접 실행 목록 화면

### 구현과 실제 확인 결과

- `get_categories()`를 재사용해 과학·역사 순서로 구분했다.
- 문제 오른쪽에 선택지 4개를 가로로 나열했다.
- 세로 구분자 없이 선택지를 공백으로 구분했다.
- 문제 사이에 빈 줄 하나를 두고 목록 뒤 메인 메뉴로 복귀했다.
- 사용자가 `main.py`에서 전체 흐름을 직접 확인해 이상 없음을 확인했다.
- `git diff --check`는 출력 없이 통과했다.

### 증거

- `evidence/screenshots/quiz-list.png`
- 기능 화면은 확인 가능하지만 계정명과 호스트명이 보여 최종 제출 전 재촬영한다.

### Git 상태

- 커밋: `5d08e39 Feat: 퀴즈 목록 조회 기능 구현`
- push: `origin/main`에 완료

### 다음 작업

- 메뉴 4번의 카테고리별 최고 점수 조회와 갱신을 구현한다.

---

## 2026-08-05 — 카테고리별 최고 점수 조회와 갱신

- 환경: macOS / zsh / Python 3.12.13
- 브랜치: `main`
- 목표: 카테고리마다 높은 플레이 점수를 메모리에 유지하고 메뉴 4번에서 조회
- 요구사항: `FUNC-14`, `FUNC-15`, `FUNC-16`

### 변경 파일

- `src/game_manager.py`: 점수 비교·갱신과 메뉴 4번 조회 구현
- `evidence/logs/best-score.md`: 사용자 직접 실행 결과 정리
- `README.md`, `docs/requirements.md`, `docs/progress.md`: 실제 상태 반영

### 구현과 실제 확인 결과

- 플레이 전 과학과 역사가 모두 `기록 없음`으로 표시됐다.
- 과학 문제 2개 중 1개 정답으로 50점을 기록했다.
- 첫 기록에서 `새로운 최고 점수: 50점` 안내가 출력됐다.
- 플레이 후 과학 50점, 미플레이 역사 `기록 없음`이 표시됐다.
- 직접 실행에서 이후 과학 0점을 받아도 최고 기록 50점이 유지됐다.
- 메뉴 5번으로 정상 종료했다.
- `git diff --check`는 출력 없이 통과했다.

### 증거

- `evidence/logs/best-score.md`

### Git 상태

- 커밋: `0da66ba Feat: 카테고리별 최고 점수 구현`
- push: `origin/main`에 완료

### 다음 작업

- 프로젝트 루트의 `state.json` 저장과 정상 데이터 불러오기를 구현한다.

---

## 2026-08-05 — state.json 저장과 정상 데이터 불러오기

- 환경: macOS / zsh / Python 3.12.13
- 브랜치: `state-json`
- 목표: 퀴즈와 카테고리별 최고 점수를 프로젝트 루트 JSON에 저장하고 시작 시 복원
- 요구사항: `FUNC-11`, `DATA-02`, `DATA-03`, `DATA-04`, `DATA-07`

### 변경 파일과 구현 내용

- `main.py`: 게임 실행 전에 `load_state()` 호출
- `src/game_manager.py`: 프로젝트 루트 경로 계산, JSON 저장·불러오기와 구조 검증
- `state.json`: 퀴즈 목록과 `best_scores`를 가진 UTF-8 초기 상태 파일 추가
- `add_quiz()`: 정상 등록 직후 `save_state()` 호출
- `update_best_score()`: 더 높은 점수로 갱신한 직후 `save_state()` 호출
- `safe_exit()`: 정상·중단 종료 전에 `save_state()` 호출
- `save_state()`: `state.json.tmp`를 먼저 쓴 뒤 `state.json`으로 교체

### 확인 상태

- 코드와 커밋에서 저장·불러오기 연결을 확인했다.
- 기능 확인 중 입력한 퀴즈와 점수가 한때 `state.json`에 반영됐고, 다음 실행
  모드 분리 작업에서 기본 문제 4개와 빈 점수의 원본 상태로 되돌렸다.
- 추가·플레이·종료·재실행 후 유지되는 전체 사용자 원본 로그는 아직 없다.
  따라서 DATA-07은 코드 구현과 직접 영속성 검증을 구분해 관리한다.

### 증거

- 새 사용자 실행 증거 없음
- JSON 적용 전 비교 기준:
  `evidence/logs/memory-persistence-test.md`

### Git 상태

- 커밋: `45990d1 Feat: state.json 저장과 불러오기 구현`
- push: `origin/state-json`에 완료

### 다음 작업

- 실제 게임 데이터와 반복 확인 데이터를 서로 다른 JSON 파일로 분리한다.

---

## 2026-08-05 — 실행 모드별 상태 파일 분리

- 환경: macOS / zsh / Python 3.12.13
- 브랜치: `state-json`
- 목표: 직접 기능 확인 중 생기는 데이터 변경이 실제 상태와 Git 커밋에 섞이지 않게 분리
- 요구사항: `DATA-02`, `DATA-07`, `SEC-01`

### 변경 파일과 구현 내용

- `src/game_manager.py`: `QUIZ_STATE_MODE`, `get_state_path()`, 실제·확인용 경로 추가
- `main.py`: 선택된 경로를 `QuizGame`에 전달하고 확인용 모드 안내 출력
- `.gitignore`: `state.test.json` 제외
- `state.json`: 기능 확인 중 추가된 임시 퀴즈와 점수를 제거하고 기본 상태로 복원

### 실행 모드

```zsh
python main.py
QUIZ_STATE_MODE=test py
```

- 환경 변수가 없거나 `real`이면 프로젝트 루트의 `state.json`을 사용한다.
- `test`이면 같은 위치의 `state.test.json`을 사용한다.
- 이 `test`는 사용자가 `main.py`를 직접 실행할 때 데이터 파일만 분리하는
  확인용 모드다.
- `.env` 파일은 추가하지 않고 현재처럼 명령 앞에 환경 변수를 지정한다.

### 확인 상태

- `state.json`이 기본 문제 4개와 빈 `best_scores`로 복원된 것을 확인했다.
- `state.test.json`은 `.gitignore`로 Git 추적에서 제외된다.
- 정상 영속성의 종료·재실행 사용자 원본 로그는 아직 필요하다.

### Git 상태

- 커밋: `40fdea5 Feat: 실행 모드별 상태 파일 분리`
- push: `origin/state-json`에 완료

### 다음 작업

- 손상된 상태 파일을 삭제하지 않고 백업한 뒤 기본 데이터로 복구한다.

---

## 2026-08-05 — 손상된 확인용 JSON 백업과 복구

- 환경: macOS / zsh / Python 3.12.13
- 브랜치: `state-json`
- 목표: 손상 원본을 보존하면서 게임을 기본 데이터로 계속 실행
- 요구사항: `DATA-05`, `DATA-06`

### 변경 파일과 구현 내용

- `src/game_manager.py`: 데이터 구조 검증, 임시 파일 정리, 손상 원본 백업,
  기본 상태 복구, 읽기·쓰기 오류 안내와 저장 비활성화 처리
- `.gitignore`: 실제·확인용 손상 백업 패턴 제외
- `evidence/screenshots/json-recovery.png`: 사용자 직접 실행 복구 화면

### 사용자 직접 실행 결과

```zsh
QUIZ_STATE_MODE=test py
```

- 확인용 JSON의 `quizzes` 키를 `quizes`로 바꾼 상태에서 실행했다.
- `상태 파일이 손상되었습니다: quizzes는 목록이어야 합니다.`가 출력됐다.
- 화면에 `state.test.json.corrupt-20260805-181939-287895` 백업 파일명이 표시됐다.
- 같은 이름의 파일이 프로젝트 루트에 실제 생성됐고, 잘못된 `quizes` 키를
  포함한 손상 원본 내용이 그대로 남아 있음을 확인했다.
- 활성 `state.test.json`은 기본 문제 4개와 빈 최고 점수로 복구되고 메뉴가
  traceback 없이 실행됐다.

### 증거

- `evidence/screenshots/json-recovery.png`
- `evidence/logs/json-recovery.md`: 캡처 출력, 백업 파일명과 실제 내용 연결

### Git 상태

- 커밋: `103a3b1 Fix: 손상된 상태 파일 백업과 복구 처리`
- push: `origin/state-json`에 완료

### 다음 작업

- 정상 확인용 데이터에서 추가 퀴즈와 최고 점수의 종료·재실행 영속성을 직접 확인한다.

---

## 2026-08-05 — 현재 구현·증거·문서 정합성 정리

- 환경: macOS / zsh
- 브랜치: `state-json`
- 목표: 현재 코드, Git, 사용자 실행 증거와 문서 설명을 같은 상태로 정리
- 요구사항: `DOC-01`~`DOC-05`, `EVID-01`~`EVID-05`

### 정리 원칙

- 사용자 제공 로그의 콘솔 내용은 다시 가공하지 않고 원형 중심으로 보존한다.
- 구현 완료, 사용자 직접 확인, 증거 확보, 미검증을 분리해 표시한다.
- 실제·확인용 데이터와 JSON 적용 전·후 영속성을 구분한다.
- 메뉴와 Git 화면의 기존 자료는 개발 과정 증거로 두고 최종본은 모든 기능과
  병합이 끝난 뒤 다시 정리한다.
- 계정명과 호스트명은 이후 사용자 지시에 따라 별도 마스킹·재촬영 조건으로
  보지 않는다. 토큰·키·인증정보 같은 비밀값은 계속 기록하지 않는다.

### 변경 파일

- `README.md`: 현재 기능, 실행 모드, 메서드, 영속성, 복구와 증거 링크 전면 갱신
- `docs/requirements.md`: JSON 요구사항의 구현·증거 상태와 검증 정책 갱신
- `docs/progress.md`: 현재 브랜치·커밋·완료·미검증·다음 작업 갱신
- `docs/architecture-plan.md`: 현재 JSON 구조와 직접 실행 검증 정책 반영
- `docs/troubleshooting.md`: 안전 종료 커밋 수정과 실제 JSON 스키마 오류 기록
- `docs/worklog.md`: JSON 관련 3개 커밋과 현재 문서 정리 과정 기록
- `evidence/logs/json-recovery.md`: 캡처와 백업 파일명·실제 손상 내용 연결

### 확인 명령과 실제 결과

```zsh
git status --short --branch
git log --oneline --decorate -8
git rev-list --count HEAD
git rev-list --count main
git diff --check
```

- 결과: 현재 브랜치는 `state-json`, 문서 정리 시작 전 로컬과
  `origin/state-json`이 `103a3b1`에서 같았다.
- 결과: 현재 브랜치는 23개, `main`은 20개 커밋이었다.
- 결과: `git diff --check`가 출력 없이 통과했다.

### Git 상태

- 현재 문서 변경: 미커밋
- commit·push: 사용자 요청이 없어 미실시

### 다음 작업

- 확인용 상태에서 정상 JSON의 종료·재실행 영속성을 사용자 직접 실행으로 검증한다.

---

## 2026-08-05 — 최고 점수 JSON 재실행 영속성 확인

- 환경: macOS / zsh / Python 3.12.13
- 브랜치: `state-json`
- 목표: 확인용 JSON에 저장된 최고 점수가 종료·재실행 후 복원되는지 직접 확인
- 요구사항: `FUNC-14`, `FUNC-15`, `DATA-07`, `EVID-03`

### 사용자 직접 실행

```zsh
QUIZ_STATE_MODE=test py
QUIZ_STATE_MODE=test py
```

### 실제 확인 결과

- 첫 실행의 점수 조회에서 과학과 역사가 모두 `기록 없음`이었다.
- 과학 문제 2개를 모두 맞혀 100점을 기록했다.
- `새로운 최고 점수: 100점` 출력 후 메뉴 5로 정상 종료했다.
- 같은 확인용 실행 명령으로 다시 시작했다.
- 두 번째 실행의 점수 조회에서 과학 `100점`, 역사 `기록 없음`이 표시됐다.
- 점검한 `state.test.json`의 `best_scores`에는 `"과학": 100`이 저장되어 있었다.
- 실제 `state.json`에 대한 `git diff`는 없었다.

### 검증 범위 구분

- 최고 점수의 JSON 저장과 재실행 복원: 확인 완료
- 추가 퀴즈의 JSON 저장과 재실행 복원: 이번 로그에 추가 과정이 없어 미검증
- 동료평가 때 같은 명령으로 직접 플레이·종료·재실행해 재검증할 수 있다.

### 증거

- `evidence/logs/persistence-restart.md`: 사용자가 제공한 두 번의 실행 원문

### Git 상태

- 검증 시작 기준 커밋:
  `02b454a Docs: JSON 구현과 검증 기록 정리`
- 시작 시 `state-json`과 `origin/state-json` 동기화, 작업 트리 깨끗함
- 현재 문서와 증거 변경: 미커밋
- commit·push: 미실시

### 다음 작업

- 확인용 상태에서 퀴즈 하나를 추가하고 종료·재실행 후 목록에 유지되는지 확인한다.

---

## 2026-08-05 — 기본 상식 퀴즈 5개 충족

- 환경: macOS / zsh
- 브랜치: `main`
- 목표: 필수 요구사항인 직접 작성 기본 퀴즈 5개 이상 충족
- 요구사항: `DATA-01`

### 변경 파일

- `src/default_quizzes.py`: 과학 기본 문제 1개 추가, 임시 데이터 설명 제거
- `state.json`: 동일한 과학 문제를 추가해 기본 생성 데이터와 실제 상태 일치
- `README.md`: `main` JSON 병합과 기본 문제 5개 상태 반영
- `docs/requirements.md`: DATA-01 구현 완료 반영
- `docs/progress.md`: 필수 데이터 완료와 다음 보너스 작업 반영
- `docs/worklog.md`: 실제 변경과 확인 결과 기록

### 추가 문제

```text
카테고리: 과학
문제: 태양계에서 가장 큰 행성은 무엇인가요?
선택지: 지구, 화성, 목성, 금성
정답: 3번 목성
```

### 확인 명령과 실제 결과

```zsh
python main.py
py
python3 --version
python3 -m json.tool state.json
rg -c '^[[:space:]]*Quiz\(' src/default_quizzes.py
rg -c '"question"' state.json
```

- 도구 셸에는 사용자 `python`, `py` 별칭이 없어 두 직접 실행 명령은 시작되지 않았다.
- 도구 셸의 `/usr/bin/python3`는 요구 버전보다 낮은 Python 3.9.6이라 게임 실행에
  사용하지 않았다.
- `python3 -m json.tool state.json`은 성공해 JSON 문법이 정상임을 확인했다.
- `src/default_quizzes.py`의 `Quiz` 생성 수와 `state.json`의 문제 수가 각각
  5개로 일치했다.
- 최종 메뉴 화면은 사용자의 Python 3.12.13 환경에서 직접 확인한다.

### Git 상태

- 작업 시작: `main`과 `origin/main`이
  `4984e31 Merge: JSON 상태 관리 브랜치 병합`에서 동기화
- commit·push: 이번 사용자 요청 범위에서 기능 확인 후 함께 수행

### 다음 작업

- 보너스 기능의 기반이 되는 풀이 문제 수 선택 기능을 구현한다.

---

## 2026-08-05 — 풀이 문제 수 선택 보너스 구현

- 환경: macOS / zsh
- 브랜치: `feature/bonus`
- 목표: 선택한 카테고리에서 원하는 수의 문제만 풀 수 있게 구현
- 요구사항: `BONUS-02`

### 변경 파일

- `src/game_manager.py`: `select_quiz_count()` 추가와 출제 목록 제한
- `README.md`: 풀이 문제 수 기능과 메서드 설명 추가
- `docs/requirements.md`: BONUS-02 구현 완료 반영
- `docs/progress.md`: 구현 내용과 다음 무작위 출제 작업 반영
- `docs/architecture-plan.md`: 플레이 흐름과 메서드 목록 갱신
- `docs/worklog.md`: 구현과 정적 확인 결과 기록

### 구현 내용

- 카테고리를 선택한 뒤 해당 카테고리의 전체 문제 수를 출력한다.
- `read_int()`를 재사용해 1부터 전체 문제 수 범위의 입력만 허용한다.
- 선택한 개수만큼 기존 문제 목록 앞부분을 잘라 저장 순서대로 출제한다.
- 결과 계산은 제한된 출제 목록의 길이를 사용하므로 정답 수와 100점 환산 점수의
  분모도 사용자가 선택한 문제 수로 자동 변경된다.
- 원본 퀴즈 목록과 JSON 스키마는 변경하지 않는다.

### 확인 명령과 실제 결과

```zsh
env PYTHONPYCACHEPREFIX=/private/tmp/codyssey-quiz-count-pycache \
  /usr/bin/python3 -m py_compile src/game_manager.py
python3 -m json.tool state.json
```

- Python 문법 컴파일이 출력 없이 성공했다.
- `state.json` 문법이 정상이고 데이터 변경이 없음을 확인했다.
- 도구 환경에는 사용자 Python 3.12.13 별칭이 없어 실제 메뉴 입력은 사용자가
  `main.py`를 직접 실행해 확인한다.

### Git 상태

- `main`의 `392afec Feat: 기본 상식 퀴즈 5개 구성`에서
  `feature/bonus` 브랜치를 생성
- 이번 요청에 따라 풀이 문제 수 선택 변경을 첫 커밋으로 정리
- `state.json`의 사용자 플레이 점수 변경은 보너스 코드 커밋에서 제외
- push와 이후 Git 조작은 사용자 직접 수행

### 다음 작업

- 선택한 문제 수만큼 원본 목록을 바꾸지 않고 무작위 출제하는 기능을 구현한다.

---

## 2026-08-05 — 문제 선택과 출제 순서 무작위화

- 환경: macOS / zsh
- 브랜치: `feature/bonus`
- 목표: 사용자가 선택한 문제 수만큼 중복 없이 뽑아 무작위 순서로 출제
- 요구사항: `BONUS-01`

### 변경 파일

- `src/game_manager.py`: 표준 라이브러리 `random`과 `random.sample()` 연결
- `README.md`: 무작위 선택·출제와 원본 순서 보존 설명
- `docs/requirements.md`: BONUS-01 구현 완료 반영
- `docs/progress.md`: 구현 상태와 다음 힌트 작업 반영
- `docs/architecture-plan.md`: 변경된 플레이 흐름 기록
- `docs/worklog.md`: 구현과 정적 확인 기록

### 구현 내용

- 카테고리 문제 객체 목록을 `random.sample()`의 모집단으로 전달한다.
- `k`에는 사용자가 앞 단계에서 선택한 문제 수를 전달한다.
- 반환된 새 목록은 선택된 문제와 순서가 모두 무작위이며 한 게임에서 중복이 없다.
- 반환된 순서 그대로 문제 번호를 붙여 출제한다.
- `self.quizzes` 원본 목록을 직접 섞거나 수정하지 않는다.
- `state.json`을 다시 쓰지 않으므로 JSON의 저장 순서도 유지된다.

### 확인 명령과 실제 결과

```zsh
env PYTHONPYCACHEPREFIX=/private/tmp/codyssey-random-quiz-pycache \
  /usr/bin/python3 -m py_compile src/game_manager.py
python3 -m json.tool state.json
```

- Python 문법 컴파일이 출력 없이 성공했다.
- `state.json` 문법이 정상이고 기본 문제 순서가 그대로임을 확인했다.
- 실제 문제 순서 변화는 사용자 Python 3.12.13 환경에서 직접 플레이해 확인한다.

### Git 상태

- Git 명령은 사용자 지시에 따라 실행하지 않음
- commit·push: 사용자 직접 수행

### 다음 작업

- 힌트 제공 방식과 힌트 사용 시 점수 차감 기준을 확정한 뒤 구현한다.

---

## 2026-08-05 — 수동 힌트와 누적 점수 구현

- 환경: macOS / zsh
- 브랜치: `feature/bonus`
- 목표: 문제별 수동 힌트와 힌트 사용에 따른 차등 점수, 결과 집계 추가
- 요구사항: `BONUS-03`

### 변경 파일

- `src/game_manager.py`: 힌트 선택·출력과 문제별 누적 점수 계산 추가
- `README.md`: 힌트 동작, 점수 기준과 이전 기록 호환성 설명
- `docs/requirements.md`: BONUS-03 구현 완료 반영
- `docs/progress.md`: 구현 상태와 다음 퀴즈 삭제 작업 반영
- `docs/architecture-plan.md`: 힌트 메서드와 플레이 흐름 갱신
- `docs/worklog.md`: 구현 내용과 정적 확인 결과 기록

### 구현 내용

- `ask_for_hint()`가 각 문제에서 힌트 보기 또는 바로 풀기를 선택받는다.
- `show_hint()`가 정답 하나와 무작위 오답 하나를 골라 두 개의 후보를 출력한다.
- 힌트 없이 정답이면 3점, 힌트 사용 후 정답이면 1점, 오답이면 0점이다.
- 힌트를 본 횟수는 정답 여부와 관계없이 `hint_count`에 누적한다.
- 결과 화면은 정답 수, 힌트 사용 횟수와 `획득 점수/출제 문제 수 × 3점`을
  출력한다.
- 최고 점수 JSON 검증 범위를 0~100에서 0 이상의 정수로 변경했다.
- 이전 100점 환산 최고 점수는 삭제하거나 변환하지 않고 그대로 불러온다.

### 확인 명령과 실제 결과

```zsh
env PYTHONPYCACHEPREFIX=/private/tmp/codyssey-hint-score-pycache \
  /usr/bin/python3 -m py_compile src/game_manager.py
python3 -m json.tool state.json
```

- Python 문법 컴파일이 출력 없이 성공했다.
- `state.json` 문법이 정상이고 `best_scores`가 빈 객체인 원본 상태를 확인했다.
- 실제 메뉴 동작은 사용자 Python 3.12.13 환경에서 직접 확인한다.

### Git 상태

- Git 명령은 사용자 지시에 따라 실행하지 않음
- commit·push: 사용자 직접 수행

### 다음 작업

- 삭제할 문제를 선택·확인하고 JSON에 즉시 반영하는 퀴즈 삭제 기능을 구현한다.

---

## 2026-08-05 — 퀴즈 삭제와 JSON 즉시 반영 구현

- 환경: macOS / zsh
- 브랜치: `feature/bonus`
- 목표: 선택한 퀴즈를 확인 후 삭제하고 활성 상태 파일에 즉시 반영
- 요구사항: `BONUS-04`

### 변경 파일

- `src/game_manager.py`: 삭제 메뉴와 `delete_quiz()` 구현
- `README.md`: 삭제 기능·메서드·저장 시점 반영
- `docs/requirements.md`: BONUS-04 구현 완료 반영
- `docs/progress.md`: 삭제 기능과 다음 점수 히스토리 작업 기록
- `docs/architecture-plan.md`: 메뉴와 삭제 흐름 갱신
- `docs/worklog.md`: 구현 내용과 정적 확인 결과 기록

### 구현 내용

- 메인 메뉴의 5번을 퀴즈 삭제, 6번을 종료로 변경했다.
- 삭제할 카테고리와 해당 카테고리의 문제 번호를 공통 숫자 입력으로 선택한다.
- 선택한 문제 내용을 다시 출력하고 삭제 또는 취소를 입력받는다.
- 삭제 확인 후 `save_state()`로 활성 상태 파일에 즉시 저장한다.
- 카테고리의 마지막 문제를 삭제하면 해당 카테고리의 최고 점수도 제거한다.
- 저장에 실패하면 퀴즈 목록과 최고 점수를 삭제 전 메모리 상태로 되돌린다.

### 확인 명령과 실제 결과

```zsh
env PYTHONPYCACHEPREFIX=/private/tmp/codyssey-delete-quiz-pycache \
  /usr/bin/python3 -m py_compile src/game_manager.py
python3 -m json.tool state.json
```

- Python 문법 컴파일이 출력 없이 성공했다.
- `state.json` 문법이 정상이며 기존 퀴즈와 최고 점수 내용은 변경하지 않았다.
- 실제 삭제·취소·재실행 동작은 사용자 Python 3.12.13 환경에서 직접 확인한다.

### Git 상태

- Git 명령은 사용자 지시에 따라 실행하지 않음
- commit·push: 사용자 직접 수행

### 다음 작업

- 날짜와 시간을 포함하는 점수 기록 히스토리의 저장 구조와 표시 방식을 설계한다.

## 2026-08-05 — 최근 플레이 기록 5개 구현

- 환경: macOS / zsh
- 브랜치: `feature/bonus`
- 목표: 모든 플레이 결과를 JSON에 저장하고 최근 5개를 메뉴에서 조회
- 요구사항: `BONUS-05`

### 변경 파일

- `src/game_manager.py`: 기록 검증·저장·최근 5개 출력과 메뉴 연결
- `README.md`: 플레이 기록 동작과 JSON 스키마 설명
- `docs/requirements.md`: BONUS-05 구현 완료 반영
- `docs/progress.md`: 보너스 구현 상태와 다음 통합 확인 작업 반영
- `docs/architecture-plan.md`: 기록 구조와 저장·조회 흐름 추가
- `docs/worklog.md`: 구현 내용과 정적 확인 결과 기록

### 구현 내용

- 플레이 완료 시 `YYYY-MM-DD HH:MM` 형식의 로컬 시각을 기록한다.
- 카테고리, 점수·만점, 정답·문제 수와 힌트 사용 횟수를 함께 저장한다.
- `record_game_result()`가 기록 추가와 최고 점수 갱신 후 JSON을 한 번 저장한다.
- 저장 실패 시 새 기록과 최고 점수를 저장 전 메모리 상태로 되돌린다.
- 메뉴 3번에서 카테고리별 최고 점수와 최근 플레이 기록을 함께 출력한다.
- JSON에는 전체 기록을 보관하고 화면에는 날짜 기준 최근 5개만 표시한다.
- 같은 분에 기록된 결과는 목록에 나중에 추가된 항목을 먼저 표시한다.
- 이전 JSON에 `score_history`가 없으면 빈 목록으로 읽어 하위 호환한다.
- 퀴즈 삭제 시 과거 플레이 기록은 유지한다.

### 확인 명령과 실제 결과

```zsh
env PYTHONPYCACHEPREFIX=/private/tmp/codyssey-score-history-pycache \
  /usr/bin/python3 -m py_compile src/game_manager.py
python3 -m json.tool state.json
```

- Python 문법 컴파일과 기존 `state.json` 문법 확인이 성공했다.
- 기존 `state.json`의 퀴즈와 최고 점수는 변경하지 않았다.
- 실제 플레이 기록 생성·최근 5개·재실행 유지는 사용자 환경에서 확인한다.

### Git 상태

- Git 명령은 사용자 지시에 따라 실행하지 않음
- commit·push: 사용자 직접 수행

### 다음 작업

- 보너스 기능 전체를 직접 실행해 기능 간 연결과 JSON 재실행 유지를 확인한다.

---

## 2026-08-05 — 메뉴·목록·삭제 확인 방식 정리

- 환경: macOS / zsh
- 브랜치: `feature/bonus`
- 목표: 관련 메뉴를 묶고 목록과 삭제 입력을 간결하게 개선

### 변경 파일

- `src/game_manager.py`: 메뉴 순서, 질문 전용 목록과 `read_yes_no()` 반영
- `README.md`: 최종 메뉴·목록·삭제 동작과 과거 목록 증거 구분
- `docs/requirements.md`: BONUS-04 직접 확인 상태와 `y/n` 입력 반영
- `docs/progress.md`: 현재 출력과 입력 방식 반영
- `docs/architecture-plan.md`: 메뉴와 세부 기능 흐름 갱신
- `docs/worklog.md`: 변경 내용과 정적 확인 결과 기록

### 구현 내용

- 메뉴를 풀기, 목록, 최고 점수, 추가, 삭제, 종료 순서로 재배치했다.
- 추가와 삭제가 각각 4번과 5번에 이어서 표시된다.
- 퀴즈 목록에서는 답안 선택지를 숨기고 카테고리별 질문만 연속 표시한다.
- 삭제 대상은 기존대로 카테고리 번호와 문제 번호로 선택한다.
- 마지막 삭제 확인은 숫자 메뉴 대신 `y/n`으로 처리한다.
- `read_yes_no()`는 앞뒤 공백과 대소문자를 정리하고 다른 입력은 다시 받는다.

### 확인 명령과 실제 결과

```zsh
env PYTHONPYCACHEPREFIX=/private/tmp/codyssey-menu-list-delete-pycache \
  /usr/bin/python3 -m py_compile src/game_manager.py
python3 -m json.tool state.json
```

- Python 문법 컴파일이 출력 없이 성공했다.
- `state.json` 문법이 정상이며 저장 데이터는 변경하지 않았다.
- 변경된 메뉴와 목록은 사용자 환경에서 직접 확인한다.
- 번호 선택과 삭제 기본 동작은 사용자가 직접 확인했다.
- 이후 변경한 최종 `y/n` 확인 방식의 실행 증거는 별도 단계에서 확보한다.

### Git 상태

- Git 명령은 사용자 지시에 따라 실행하지 않음
- commit·push: 사용자 직접 수행

### 다음 작업

- 날짜와 시간을 포함하는 점수 기록 히스토리의 저장 구조와 표시 방식을 설계한다.

---

## 2026-08-05 — 보너스 main 병합 후 문서 정합성 갱신

- 환경: macOS / zsh
- 브랜치: `main`
- 목표: 필수·보너스 구현 완료 상태와 원본 로그 보존 원칙을 문서에 반영

### 확인한 현재 상태

- 사용자가 `feature/bonus` 작업의 `main` 병합을 완료했다.
- 정확한 병합 커밋 해시와 최종 그래프는 증거 확보 단계에서 사용자가 확인한다.
- 필수 기능과 BONUS-01~05 구현 내용은 코드와 문서에 연결되어 있다.
- 실제 작업 순서는 메뉴·목록·삭제 확인 방식 정리 후 최근 플레이 기록 구현이다.
  같은 날짜의 기존 상세 항목 배치보다 이 순서를 현재 진행 기준으로 사용한다.

### 갱신 파일

- `README.md`: `main` 병합, 최종 데이터 범위, 저장 시점과 남은 증거 반영
- `docs/architecture-plan.md`: 구현 완료된 보너스 범위와 최종 단계 반영
- `docs/requirements.md`: 최종 무작위 출제와 보너스 검증 상태 정정
- `docs/progress.md`: 현재 단계, 플레이 기록 복원과 사용자 병합 상태 반영
- `docs/worklog.md`: 병합 이후 문서 정합성 점검 기록
- `evidence/logs/best-score.md`: 사용자가 제공한 셸 프롬프트 원문 복원
- `evidence/logs/safe-exit.md`: 터미널 캡처의 셸 프롬프트 원문 복원

### 원본 로그 보존

- 사용자가 제공한 로그는 계정명·호스트명을 임의 치환하거나 실행 결과를
  재구성하지 않는다.
- 설명이 필요하면 원문 코드 블록 밖에 작성한다.
- 원문을 확보하지 못한 항목은 실행한 것처럼 새로 만들지 않고 증거 예정으로 둔다.
- `memory-persistence-test.md`의 `$` 프롬프트는 당시 원문이 남아 있지 않아
  임의 복원하지 않고 제한 사항을 문서에 명시했다.

### Git 상태

- merge: 사용자 완료
- Git 명령: 사용자 지시에 따라 실행하지 않음
- commit·push 및 병합 해시: 이번 문서 갱신에서는 확인하지 않음

### 다음 작업

- 별도 단계에서 최종 기능 실행, 영속성, Git 그래프와 clone·pull 증거를
  원문 로그·캡처로 확보한다.

---

## 2026-08-06 — 테스트 기록 정리와 점수·히스토리 표시 개선

- 환경: Linux / bash / Python 3.12.3 격리 복사본
- 브랜치: `main`
- 목표: 현재 기능과 맞지 않는 테스트 자료를 정리하고 점수·히스토리 출력과
  추적 JSON 스키마를 현재 구현에 맞춘다.
- 요구사항: `FUNC-07`, `DATA-02`, `BONUS-03`, `BONUS-05`

### 변경 파일

- `tests/`: 기존 유닛테스트 파일과 디렉터리 전체 삭제
- `AGENTS.md`, `README.md`, `docs/*.md`: 유닛테스트 정책·파일·실행 결과 기록 제거
- `src/game_manager.py`: 결과와 최근 기록에서 만점 없이 획득 점수만 출력
- `state.json`: 빈 `score_history` 목록을 기본 스키마에 추가
- `README.md`: 표준 `python3 main.py` 실행 명령과 현재 점수 표시 방식 반영
- `docs/progress.md`, `docs/requirements.md`: 현재 상태와 다음 수정 작업 반영
- `docs/troubleshooting.md`: 히스토리 필드 누락 원인과 해결 기록

### 구현과 확인 결과

- 점수 계산과 최고 점수 비교는 기존 원점수 방식을 유지했다.
- `max_score`는 플레이 기록 검증을 위해 JSON 내부에 유지하고 화면에서는 숨겼다.
- 히스토리 커밋 `4da450f`는 정상 병합됐으며 `state.json` 갱신만 누락된 것을
  Git 이력으로 확인했다.
- 유닛테스트 관련 문구와 파일 참조가 남아 있지 않은지 전체 텍스트를 확인했다.
- 필수 제출 증거 파일은 만들거나 변경하지 않았다.

### 실행 명령과 실제 결과

다음 플레이·문법 확인 명령은 원본 상태를 바꾸지 않도록 격리 복사본에서
실행했고, `git diff --check`는 원본 저장소에서 실행했다.

```bash
python3 -m compileall -q main.py src
python3 -m json.tool state.json
printf '1\n2\n1\n2\n1\n3\n6\n' | python3 main.py
printf '3\n6\n' | python3 main.py
git diff --check
```

- Python 문법과 JSON 문법이 정상임을 확인했다.
- 결과 화면과 최근 기록에 획득 점수만 표시됐다.
- 플레이 기록이 JSON에 저장되고 재실행 후 다시 표시됐다.
- `git diff --check`가 출력 없이 통과했다.

### Git 상태

- 구현 커밋: `81dddf1 Refactor: 테스트 기록 정리와 점수·히스토리 표시 개선`
- 구현 push: `origin/main`에 완료
- 현재 작업 기록과 다음 작업 문서 갱신: 미커밋
- 문서 갱신 권장 커밋 메시지:
  `Docs: 현재 작업 기록과 다음 개선 사항 갱신`

### 다음 작업

1. `Quiz`와 JSON에 문제별 힌트 문장을 저장하고 `show_hint()`가 해당 문장을
   출력하도록 변경한다.
2. 퀴즈 추가 직후 저장에 실패했을 때 새 퀴즈를 메모리에 유지할지 제거할지
   결정하고 `add_quiz()`의 실패 처리를 정리한다.
## 2026-08-06 — 문제별 JSON 저장 힌트 구현

- 환경: macOS / zsh
- 브랜치: `main`
- 목표: 두 선택지 후보 방식의 힌트를 각 문제에 저장된 문장형 힌트로 변경
- 요구사항: `BONUS-03`, `DATA-02`, `DATA-03`

### 작업 시작 상태

- `main`과 로컬 추적 기준 `origin/main`은 `c362ed7`에서 일치했다.
- 작업 트리는 깨끗했다.
- 사용자 승인 후 저장형 힌트 범위만 구현했다.

### 변경 파일

- `src/quiz.py`: 선택적 `hint` 속성과 검증·JSON 변환·복원 추가
- `src/default_quizzes.py`: 기본 문제 5개에 직접 작성한 힌트 추가
- `src/game_manager.py`: 기존 기본 문제의 힌트 보완, 새 퀴즈 힌트 입력,
  저장된 힌트 출력과 힌트 미등록 시 점수 비차감 처리
- `state.json`: 기본 퀴즈 5개의 `hint` 필드 추가
- `README.md`, `docs/requirements.md`, `docs/progress.md`: 구현 상태와 스키마 반영

### 기존 JSON 호환

- `hint` 필드가 없는 기존 JSON도 손상 데이터로 판정하지 않는다.
- 카테고리와 질문이 기본 문제와 일치하면 기본 데이터의 힌트를 연결한다.
- 일치하지 않는 기존 사용자 추가 문제는 힌트 미등록 안내 후 힌트 사용으로
  계산하지 않아 점수를 차감하지 않는다.

### 실행 명령과 실제 결과

```zsh
python3 -c 'import json; from src.default_quizzes import get_default_quizzes; from src.game_manager import QuizGame; from src.quiz import Quiz; defaults=get_default_quizzes(); legacy=[q.to_dict() for q in defaults]; [item.pop("hint") for item in legacy]; loaded=[Quiz.from_dict(item) for item in legacy]; game=QuizGame(quizzes=defaults, output_func=lambda message: None); game.restore_missing_default_hints(loaded); assert all(q.hint for q in loaded); unknown=Quiz("기타", "기존 문제", ["1", "2", "3", "4"], 1); assert game.show_hint(unknown) is False; assert all("hint" in q.to_dict() for q in defaults); json.load(open("state.json", encoding="utf-8")); [compile(open(path, encoding="utf-8").read(), path, "exec") for path in ("main.py", "src/__init__.py", "src/quiz.py", "src/default_quizzes.py", "src/game_manager.py")]; print("힌트 직렬화·기존 JSON 호환·Python/JSON 문법 확인 완료")'
git diff --check
```

- 힌트 직렬화, 기존 기본 문제의 힌트 보완과 힌트 미등록 시 반환값을 확인했다.
- Python 파일 5개 문법과 `state.json` JSON 형식을 확인했다.
- 사용자가 `main.py`에서 문제별 힌트와 점수 동작을 직접 확인했다.

### Git 상태

- commit: `c2321df Feat: 문제별 힌트 저장 방식 개선`
- push: `origin/main`에 완료

### 다음 작업

- 퀴즈 추가 저장 실패 시 메모리와 JSON 상태를 일치시키는 롤백을 검토한다.

---

## 2026-08-06 — 퀴즈 추가 저장 실패 시 메모리 복구

- 환경: macOS / zsh
- 브랜치: `main`
- 목표: JSON 저장에 실패한 새 퀴즈가 현재 실행의 메모리에 남지 않도록 처리
- 요구사항: `FUNC-11`, `DATA-06`

### 작업 시작 상태

- 문제별 저장 힌트를 사용자가 직접 확인했다.
- 힌트 작업은 `c2321df Feat: 문제별 힌트 저장 방식 개선`로 push됐다.
- `main`과 로컬 추적 기준 `origin/main`이 일치하고 작업 트리가 깨끗했다.

### 변경 파일

- `src/game_manager.py`: `add_quiz()`가 성공 여부를 반환하고 저장 실패 시 방금
  추가한 퀴즈를 메모리 목록에서 제거하도록 변경
- `README.md`, `docs/architecture-plan.md`, `docs/requirements.md`,
  `docs/progress.md`: 저장 실패 처리와 현재 확인 상태 반영
- `docs/worklog.md`: 구현 범위와 실제 검사 결과 기록

### 동작 기준

- 메모리 추가와 JSON 저장이 모두 성공해야 퀴즈 추가 성공으로 처리한다.
- JSON 저장에 실패하면 기존 퀴즈 목록은 유지하고 새 퀴즈만 제거한다.
- 실패 메시지는 `파일에 저장하지 못해 퀴즈 추가를 취소했습니다.`로 안내한다.

### 개선 배경

- 코드 검토 중 `save_state()` 실패 후 메모리와 JSON 상태가 달라질 가능성을
  확인했다.
- 파일 권한 부족이나 저장 경로 문제로 저장이 실패하면 같은 실행에는 새 퀴즈가
  보이지만, 재실행 후에는 파일에 없어서 사라진 것처럼 보일 수 있다.
- 저장 실패 시 방금 추가한 퀴즈를 롤백해 JSON 저장 성공 여부와 실제 추가 결과가
  일치하도록 개선했다.
- 실제 사용자 장애를 재현해 해결한 기록은 아니므로 `docs/troubleshooting.md`에는
  추가하지 않고 예방적 개선 사항으로 작업 로그에 기록한다.

### 실행 명령과 실제 결과

```zsh
python3 -c 'import json, tempfile; from pathlib import Path; from src.game_manager import QuizGame; from src.quiz import Quiz; values=["테스트", "저장 확인 문제", "가", "나", "다", "라", "2", "두 번째 선택지입니다."]; outputs=[]; tmp=tempfile.TemporaryDirectory(); path=Path(tmp.name)/"state.json"; game=QuizGame(state_path=path, input_func=lambda prompt: values.pop(0), output_func=outputs.append); assert game.add_quiz() is True; saved=json.loads(path.read_text(encoding="utf-8")); assert len(game.quizzes)==1 and saved["quizzes"][0]["hint"]=="두 번째 선택지입니다."; base=Quiz("기존", "기존 문제", ["1", "2", "3", "4"], 1, "기존 힌트"); fail_values=["테스트", "실패 문제", "가", "나", "다", "라", "2", "실패 힌트"]; fail_outputs=[]; failed_game=QuizGame(quizzes=[base], input_func=lambda prompt: fail_values.pop(0), output_func=fail_outputs.append); failed_game.save_state=lambda: False; assert failed_game.add_quiz() is False; assert failed_game.quizzes==[base]; assert fail_outputs[-1]=="파일에 저장하지 못해 퀴즈 추가를 취소했습니다."; tmp.cleanup(); print("정상 저장과 저장 실패 메모리 복구 확인 완료")'
git diff --check
```

- 임시 디렉터리에서는 정상 추가 후 메모리와 JSON에 같은 힌트가 저장됐다.
- 저장 실패를 주입한 게임에서는 반환값이 `False`였고 기존 퀴즈만 남았다.
- 실패 안내 문구가 예상과 일치했다.
- 정상 추가 흐름은 사용자 확인을 거쳤고, 저장 실패 경로는 격리 검사로 확인했다.

### Git 상태

- 구현 commit: `9287f22 Fix: 퀴즈 추가 저장 실패 처리 개선`
- 문서 commit: `a624524 Docs: 퀴즈 추가 롤백 개선 배경 보완`
- push: 두 커밋 모두 `origin/main`에 완료

### 다음 작업

- 카테고리 없는 단일 상식 퀴즈 구조로 단순화한다.

---

## 2026-08-06 — 단일 상식 퀴즈 구조로 단순화

- 환경: macOS / zsh / Python 3.12.13
- 브랜치: `main`
- 목표: 카테고리 구분과 과거 테스트용 범용 입출력 주입을 제거
- 요구사항: `TECH-02`, `TECH-05`, `FUNC-05`, `FUNC-09`, `FUNC-14`, `DATA-02`

### 작업 시작 상태

- `main`과 로컬 추적 기준 `origin/main`은 `a624524`에서 일치했다.
- 작업 트리는 깨끗했다.
- 제한 시간·자동 힌트 기능은 설계만 검토하고 구현을 보류했다.

### 변경 파일

- `src/quiz.py`: `category`와 출력 함수 주입을 제거하고 `print()`로 직접 출력
- `src/default_quizzes.py`: 기본 문제의 카테고리 인자 제거
- `src/game_manager.py`: 카테고리 선택·그룹 메서드 제거, 전체 문제 기반
  플레이·목록·삭제, 단일 최고 점수와 직접 `input()`·`print()` 구조로 변경
- `state.json`: 퀴즈의 `category`와 `best_scores`를 제거하고 `best_score` 사용
- `README.md`, `docs/architecture-plan.md`, `docs/requirements.md`,
  `docs/progress.md`: 단일 상식 퀴즈 구조와 새 JSON 스키마 반영

### 기존 JSON 호환

- 이전 퀴즈와 플레이 기록의 `category` 필드는 읽을 때 무시한다.
- 이전 `best_scores` 객체의 값 중 최댓값을 단일 `best_score`로 이전한다.
- 다음 저장부터 카테고리 필드가 없는 새 스키마로 기록한다.

### 실행 명령과 실제 결과

```zsh
python3 -c 'import json; from pathlib import Path; files=[Path("main.py"), *Path("src").glob("*.py")]; [compile(p.read_text(encoding="utf-8"), str(p), "exec") for p in files]; state=json.loads(Path("state.json").read_text(encoding="utf-8")); assert "best_score" in state and "best_scores" not in state; assert all("category" not in quiz for quiz in state["quizzes"]); print(f"Python syntax OK: {len(files)} files"); print("single-quiz state schema OK")'
python3 - <<'PY'
import json
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from src.default_quizzes import get_default_quizzes
from src.game_manager import QuizGame

legacy_state = {
    "quizzes": [{
        "category": "과학",
        "question": "물의 화학식은 무엇인가요?",
        "choices": ["CO2", "H2O", "O2", "NaCl"],
        "answer": 2,
        "hint": "물 힌트",
    }],
    "best_scores": {"과학": 4, "역사": 7},
    "score_history": [{
        "played_at": "2026-08-05 21:34",
        "category": "과학",
        "score": 4,
        "max_score": 6,
        "correct_count": 2,
        "total_count": 2,
        "hint_count": 1,
    }],
}

with tempfile.TemporaryDirectory() as temp_dir:
    state_path = Path(temp_dir) / "state.json"
    state_path.write_text(json.dumps(legacy_state, ensure_ascii=False), encoding="utf-8")
    game = QuizGame(get_default_quizzes(), state_path)
    assert game.load_state() is True
    assert game.best_score == 7
    assert not hasattr(game.quizzes[0], "category")
    assert "category" not in game.score_history[0]

    answers = ["새 문제", "가", "나", "다", "라", "2", "새 힌트"]
    with patch("builtins.input", side_effect=answers), redirect_stdout(StringIO()):
        assert game.add_quiz() is True

    with patch("src.game_manager.random.sample", return_value=[game.quizzes[0]]):
        with patch("builtins.input", side_effect=["1", "2", "2"]):
            with redirect_stdout(StringIO()):
                assert game.play_quizzes() == 3

    saved = json.loads(state_path.read_text(encoding="utf-8"))
    assert "best_score" in saved and "best_scores" not in saved
    assert all("category" not in quiz for quiz in saved["quizzes"])
    assert all("category" not in record for record in saved["score_history"])

print("legacy migration, add, play, score save OK")
PY
git diff --check
```

- Python 파일 5개 문법과 추적 `state.json`의 새 스키마가 정상이다.
- 구형 카테고리 JSON에서 최고 점수 7점과 플레이 기록을 복원했다.
- 새 퀴즈 추가와 전체 목록 기반 플레이 후 새 스키마 저장을 확인했다.
- 직접 `input()`을 패치한 임시 검사에서 추가 저장 실패, 삭제 저장 실패의
  메모리 롤백과 마지막 퀴즈 삭제 시 단일 최고 점수 초기화를 확인했다.
- `git diff --check`에서 공백 오류가 발견되지 않았다.
- 사용자가 변경된 단일 상식 퀴즈 흐름을 직접 실행하고 문제가 없음을 확인했다.
- 별도 원본 로그나 캡처는 이번 확인에서 추가되지 않았다.

### Git 상태

- commit: `8f5b8b7 Refactor: 카테고리 분류 제거`
- push: `origin/main`에 완료

### 다음 작업

- 제한 시간·자동 힌트 구현 전에 현재 코드와 문서 정합성을 점검한다.

---

## 2026-08-06 — 최신 커밋과 문서 정합성 점검

- 환경: macOS / zsh / Python 3.12.13
- 브랜치: `main`
- 목표: 오늘 작업 기록을 최신 코드·Git 상태와 사용자 확인 결과에 맞춘다.
- 대상: `README.md`, `docs/architecture-plan.md`, `docs/requirements.md`,
  `docs/progress.md`, `docs/worklog.md`

### 점검 시작 상태

- 작업 트리는 깨끗했다.
- `main`과 `origin/main`은
  `8f5b8b7 Refactor: 카테고리 분류 제거`에서 일치했다.
- 사용자는 카테고리 없는 단일 상식 퀴즈 흐름에 문제가 없음을 직접 확인했다.
- 이번 확인의 별도 원본 로그나 캡처는 제공되지 않았다.

### 확인한 오늘의 커밋

- `81dddf1 Refactor: 테스트 기록 정리와 점수·히스토리 표시 개선`
- `c362ed7 Docs: 작업 상황 기록 및 다음 개선 사항 갱신`
- `c2321df Feat: 문제별 힌트 저장 방식 개선`
- `9287f22 Fix: 퀴즈 추가 저장 실패 처리 개선`
- `a624524 Docs: 퀴즈 추가 롤백 개선 배경 보완`
- `8f5b8b7 Refactor: 카테고리 분류 제거`

### 발견한 차이와 갱신 내용

- README와 진행 문서의 `직접 확인 대기`, `미커밋` 상태를 실제 확인·push 완료로
  변경했다.
- 요구사항 추적표의 전체 상식 퀴즈 출제·추가·단일 최고 점수·문제 수 선택·힌트·
  삭제 상태를 사용자 확인 결과에 맞춰 갱신했다.
- 저장 실패 롤백은 정상 추가의 사용자 확인과 실패 경로의 격리 검증을 구분해
  `부분 검증`으로 유지했다.
- 작업 로그에 실제 커밋 해시와 push 완료 상태를 반영했다.
- 아키텍처의 카테고리 제거 권장 커밋 문구를 실제 커밋으로 교체했다.
- 새 오류를 해결한 작업이 아니므로 `docs/troubleshooting.md`는 변경하지 않았다.

### 실행 명령과 실제 결과

```zsh
git status --short --branch
git log --oneline --decorate -8
git log --since='2026-08-06 00:00:00 +0900' --date=iso-local --pretty=format:'%h%x09%ad%x09%s'
git show --stat --oneline --decorate 8f5b8b7
git rev-list --count HEAD
git branch --all --no-color
git log --oneline --graph --decorate --all -15
rg -n '^(from|import) ' main.py src/*.py
rg -n '직접 확인 필요|직접 확인 대기|push가 다음|현재 미커밋' README.md docs/*.md
git diff --check
```

- 점검 시작 시 브랜치와 원격 추적 브랜치는 `8f5b8b7`에서 일치했다.
- 오늘 커밋 6개와 최신 커밋의 변경 파일 9개를 확인했다.
- 현재 커밋은 총 41개이며 기능·상태 관리 브랜치와 병합 이력이 남아 있다.
- Python import는 모두 표준 라이브러리와 프로젝트 내부 모듈이다.
- 현재 코드·스키마와 맞지 않는 구현 설명은 발견되지 않았다.
- 상태가 오래된 문구를 실제 확인·Git 상태에 맞춰 갱신했다.
- `git diff --check`는 출력 없이 통과했다.

### Git 상태

- 코드 변경: 없음
- 문서 변경: 커밋 전
- 권장 커밋 메시지: `Docs: 최신 작업 상태와 검증 결과 갱신`

### 다음 작업

- 제한 시간·자동 힌트 구조의 수정 대상과 테스트 기준을 현재 코드에 맞춰 다시
  설명하고, 사용자 승인 후 구현한다.

---

## 2026-08-06 — 제한 시간과 자동 힌트 실험 구현

- 환경: macOS / zsh / Python 3.12.13
- 브랜치: `Test/time-limit`
- 목표: 문제마다 20초 제한 시간, 10초 자동 힌트와 한 줄 카운트다운을 실험한다.
- 요구사항: `BONUS-03`, `BONUS-06`, `BONUS-07`

### 작업 시작 상태

- 사용자가 실험용 `Test/time-limit` 브랜치를 미리 만들고 체크아웃했다.
- 작업 트리는 깨끗했다.
- 브랜치 시작 커밋은
  `ba58b00 Docs: 최신 작업 상태와 검증 결과 갱신`이었다.

### 변경 파일

- `src/timed_input.py`: `select`, `time.monotonic`, 현재 줄 갱신과 `termios`를
  사용하는 20초 제한 시간 입력 구현
- `src/game_manager.py`: 수동 힌트 선택 제거, 자동 힌트 결과에 따른 3점·1점·0점
  계산과 시간 초과 흐름 연결
- `README.md`, `docs/architecture-plan.md`, `docs/requirements.md`,
  `docs/progress.md`: 실험 구조·상태·직접 확인 항목 반영
- `docs/worklog.md`: 실제 구현과 격리 검사 결과 기록

### 구현 동작

- 각 문제를 출력한 뒤 20초부터 새 카운트다운을 시작한다.
- 대화형 터미널에서는 현재 입력 줄의 `남은 시간 | 정답 번호`를 다시 그린다.
- 10초가 되면 해당 문제의 JSON 힌트를 자동 공개한다.
- 10초 전 정답은 3점, 이후 정답은 1점, 오답·시간 초과는 0점이다.
- 빈 입력·문자·범위 밖 숫자는 타이머를 초기화하지 않고 다시 입력받는다.
- 20초 시간 초과 시 입력 큐를 비워 이전 문제 입력이 다음 문제와 섞이지 않게 한다.
- JSON 스키마는 바꾸지 않고 기존 `hint_count`를 자동 힌트 공개 횟수로 사용한다.

### 실행 명령과 실제 결과

```zsh
python3 -m py_compile main.py src/*.py
git diff --check
```

- Python 문법 검사와 공백 오류 검사가 통과했다.
- `pty.openpty()` 기반 임시 검사에서 다음 결과를 확인했다.
  - `PTY fast/hint/invalid/timeout-input-flush cases OK`
  - `PTY one-line countdown and automatic hint display OK`
  - `QuizGame 3/1/0 scoring and automatic-hint history OK`
  - `integrated PTY menu/play/save/exit flow OK`
  - `timed-input KeyboardInterrupt safe-exit OK`
- 빠른 정답, 힌트 후 정답, 잘못된 입력 후 재입력과 무입력 시간 초과를 확인했다.
- 3초 단축 검사에서 `3초 → 2초 → 1초`가 같은 줄에 갱신되고 힌트가 자동
  공개되는 것을 확인했다.
- 첫 문제에서 `2`만 입력하고 Enter 없이 시간 초과한 뒤 두 번째 문제에 `3`을
  입력했을 때 `23`이 아니라 `3`만 처리됐다.
- 제한 시간 입력 대기 중 `KeyboardInterrupt`가 발생해도 traceback 없이 상태를
  저장하고 종료 안내를 출력했다.
- 실제 20초 설정의 `main.py` 사용자 실행은 아직 미검증이다.

### Git 상태

- 구현·문서: 미커밋
- push: 미실시
- 권장 커밋 메시지: `Feat: 제한 시간과 자동 힌트 기능 실험`

### 다음 작업

- 사용자가 확인용 JSON으로 실제 20초 카운트다운, 10초 자동 힌트, 점수와
  문제별 시간 초기화를 macOS 터미널에서 직접 확인한다.

---

## 2026-08-06 — 카운트다운의 문제 영역 덮어쓰기 수정

- 환경: macOS 터미널 / zsh
- 브랜치: `Test/time-limit`
- 관련 요구사항: `BONUS-06`, `BONUS-07`

### 실제 증상과 원인

- 사용자가 실제 터미널에서 실행했을 때 남은 시간이 매초 위쪽 줄로 이동하면서
  선택지와 문제를 지우고, 타이머 출력이 여러 줄에 남았다.
- 최초 구현은 ANSI 커서 저장·복원 뒤 위쪽 타이머 줄로 이동하는 방식이었다.
- 터미널에서 저장·복원 시퀀스가 기대대로 처리되지 않으면 복원되지 않은 현재
  위치를 기준으로 다음 갱신이 다시 위로 이동해 문제 영역까지 덮을 수 있었다.

### 변경 내용

- 커서 저장·복원과 위쪽 이동 시퀀스를 모두 제거했다.
- 타이머와 답 입력을 `남은 시간 | 정답 번호` 한 줄에 함께 표시하고 `\r`과
  현재 줄 지우기만 사용해 같은 줄을 다시 그린다.
- `termios`로 입력 중에 canonical mode와 echo를 잠시 끄고, `os.read()`로 받은
  문자를 내부 버퍼에 보관해 타이머 갱신 중에도 입력 내용이 사라지지 않게 했다.
- 답 제출·시간 초과·EOF·`KeyboardInterrupt` 모든 종료 경로에서 원래 터미널
  설정을 복원한다.
- `select`와 텍스트 스트림 버퍼가 서로 다른 입력 상태를 볼 수 있으므로 대화형
  입력은 `sys.stdin.read()` 대신 `os.read()`를 사용한다.

### 재검증 결과

```zsh
python3 -m py_compile main.py src/*.py
python3 -m json.tool state.json >/dev/null
git diff --check
```

- 문법, JSON, 공백 검사가 통과했다.
- PTY 격리 검사 결과:
  - `PTY fast/hint/invalid/timeout-isolation/interrupt cases OK`
  - `No cursor-up or cursor-save escape sequences emitted`
- 빠른 정답, 자동 힌트 후 정답, 잘못된 입력 후 재입력, 첫 문제의 Enter 없는
  입력이 다음 문제와 분리되는 동작과 `KeyboardInterrupt`를 확인했다.
- 실제 macOS 터미널에서 수정된 화면 갱신 동작은 사용자 재확인이 필요하다.

---

## 2026-08-06 — 힌트 전용 줄의 제자리 갱신

- 환경: macOS 터미널 / zsh
- 브랜치: `Test/time-limit`
- 목표: 힌트가 공개될 때 입력 줄이 아래로 밀리지 않게 한다.

### 사용자 확인과 변경 내용

- 사용자가 현재 줄 방식에서 문제와 선택지가 지워지지 않는 것을 직접 확인했다.
- 문제 시작 시 안내 문장 대신 내용이 비어 있는 `힌트:` 줄을 출력한다.
- 10초가 되면 커서 저장·복원 없이 바로 위의 전용 줄만 실제 힌트로 교체하고,
  같은 횟수만큼 아래로 이동해 타이머·입력 줄로 돌아온다.
- 매초 타이머 갱신은 계속 현재 입력 줄에서만 수행한다.
- 입력 문자는 비정규·비에코 모드의 내부 버퍼에 있으므로 타이머 갱신과 힌트
  교체 전후에 같은 내용으로 다시 표시한다.

### 재검증 결과

```zsh
python3 -m py_compile main.py src/*.py
git diff --check
```

- `PTY reserved-hint-line and buffered-digit preservation OK`
- `Hint uses one balanced up/down update; timer uses current line only`
- 숫자 `2`를 Enter 없이 입력하고 초 갱신과 힌트 공개를 기다린 뒤에도 입력 줄에
  `2`가 유지됐고, 이후 Enter를 누르면 `answer=2`, `hint_shown=True`로 처리됐다.
- 초기 화면에는 `힌트:`만 출력되고 기존 자동 공개 안내 문장은 출력되지 않았다.
- 수정 화면의 실제 macOS 터미널 동작은 사용자 재확인이 필요하다.

---

## 2026-08-06 — 잘못된 입력 메시지를 하단 전용 줄에서 갱신

- 환경: macOS 터미널 / zsh
- 브랜치: `Test/time-limit`
- 목표: 오류 메시지가 힌트 아래에 누적되어 힌트와 입력 줄이 멀어지는 현상을
  없앤다.

### 사용자 확인과 변경 내용

- 사용자가 빈 힌트 줄의 제자리 갱신과 입력 유지 동작을 직접 확인했다.
- 문제 시작 화면은 `힌트:`와 `남은 시간 | 정답 번호` 두 줄만 유지한다.
- 첫 잘못된 입력이 제출되면 입력 줄 바로 아래에 오류 전용 줄을 한 번 만든다.
- 다음 잘못된 입력부터는 새 줄을 출력하지 않고 기존 오류 줄을 덮어쓴다.
- 힌트와 타이머·입력 줄은 기존 위치를 유지하며, 힌트 공개와 입력 문자 보존도
  이전 동작을 그대로 유지한다.
- 정답 제출, 시간 초과와 `KeyboardInterrupt` 때 오류 전용 줄을 지우고 패널
  다음 줄에서 결과 또는 종료 안내를 출력한다.

### 재검증 결과

```zsh
python3 -m py_compile main.py src/*.py
python3 -m json.tool state.json >/dev/null
git diff --check
```

- 반복해서 잘못 입력한 뒤 힌트 공개와 타이머 갱신이 이어져도 오류 갱신이 하단
  전용 줄을 대상으로 하는 ANSI 출력 순서를 확인했다.
- 오류 후 숫자 `2`를 Enter 없이 유지하고 힌트 공개 뒤 제출했을 때
  `answer=2`, `hint_shown=True`로 처리됐다.
- 오류가 표시된 상태의 시간 초과 후 두 번째 문제 답이 섞이지 않았고,
  `KeyboardInterrupt`에서도 터미널 설정과 화면 종료 경로가 정상 처리됐다.
- 실제 macOS 터미널에서 최종 세 줄 배치는 사용자 재확인이 필요하다.

---

## 2026-08-06 — 제한 시간 브랜치 전체 점검과 병합 준비

- 환경: macOS / zsh / Python 3.12.13 / Git 2.53.0
- 브랜치: `Test/time-limit`
- 목표: 미션 필수사항, 코드·문서·증거 정합성과 `main` 병합 가능 여부를 확인한다.

### Git과 사용자 확인 상태

- 점검 시작 시 작업 트리는 깨끗했다.
- `Test/time-limit`과 `origin/Test/time-limit`은 다음 커밋에서 일치했다.
  - `e53b9cf Feat: 제한 시간과 자동 힌트 기능 실험`
  - `ddc2d8e Fix: 힌트와 오류 메시지 출력 위치 안정화`
- `main`과 `origin/main`은 분기 기준인
  `ba58b00 Docs: 최신 작업 상태와 검증 결과 갱신`에서 일치했다.
- 사용자가 실제 macOS 터미널에서 카운트다운, 힌트 제자리 공개, 입력 유지와
  하단 오류 줄 갱신이 원하는 방식으로 동작함을 확인했다.
- 점검 시작 기준 전체 커밋 수는 44개로 최소 10개 요구를 충족했다.

### 미션·코드 회귀 검사

```zsh
python3 --version
git --version
python3 -m py_compile main.py src/*.py
python3 -m json.tool state.json >/dev/null
git diff --check
```

- Python 3.12.13과 Git 2.53.0을 확인했다.
- Python 문법, JSON 형식과 Git 공백 검사가 통과했다.
- AST import 검사에서 외부 패키지 없이 Python 표준 라이브러리와 프로젝트 내부
  모듈만 사용하는 것을 확인했다.
- `Quiz`, `QuizGame` 클래스와 직접 작성한 상식 퀴즈 5개, 선택지 4개와 힌트를
  확인했다.
- 임시 디렉터리에서 다음 필수 흐름이 통과했다.
  - 상태 파일 없음 시 기본 데이터 저장
  - 한글 퀴즈 추가와 재실행 복원
  - 빈 값·문자·범위 밖 숫자·공백 포함 숫자 검증
  - 실제 저장 경로 오류 시 퀴즈 추가 롤백
  - 손상 JSON 백업과 기본 데이터 복구
  - 빈 퀴즈 플레이·목록 안내
  - EOF 안전 종료
- 격리 점수 검사에서 힌트 전 정답 3점, 힌트 후 정답 1점, 시간 초과·오답
  0점과 플레이 기록 저장을 확인했다.
- PTY 검사에서 힌트·타이머·하단 오류 줄, 입력값 유지, 시간 초과 입력 분리와
  `KeyboardInterrupt` 뒤 터미널 정리가 통과했다.
- 필수 기능이나 확정된 제한 시간 명세와 충돌하는 코드는 발견하지 못했다.

### 문서에서 바로잡은 차이

- 제한 시간 기능이 미커밋이라는 이전 기록을 실제 두 커밋과 원격 동기화 상태로
  갱신했다.
- 사용자 재확인 대기를 실제 직접 확인 완료로 갱신했다.
- 힌트가 없는 과거 사용자 문제도 10초 이후에는 시간 규칙에 따라 1점이라는
  현재 코드 동작으로 진행 문서를 바로잡았다.
- 점검 당시 `state.json`에는 제한 시간 확인 중 생성된 플레이 기록 2개가 있었고
  스키마에는 맞았다. 이후 사용자 요청에 따라 기본 퀴즈 5개는 유지하고
  `best_score: null`, `score_history: []`인 미플레이 초기 상태로 정리했다.

### 증거 점검

- 확보됨: Python·Git 버전 화면, 과거 브랜치 병합, 안전 종료, JSON 손상 복구,
  과거 최고 점수 영속성 로그. 환경 화면에서 VSCode 사용 맥락이 충분히 보이는지는
  최종 캡처 때 보완한다.
- 기존 `menu-test.png`, `quiz-list.png`, `best-score.md`, `safe-exit.png` 일부는
  카테고리와 메뉴 1~5를 사용하던 과거 화면이므로 개발 과정 증거로만 유지한다.
- 최종 제출용으로 아직 필요한 증거:
  - 현재 메뉴 1~6
  - 퀴즈 추가와 재실행 후 목록 유지
  - 현재 목록·삭제·최고 점수·최근 기록
  - 20초 플레이, 10초 자동 힌트와 3점·1점·0점 결과
  - 병합 후 최종 Git 그래프
  - 별도 디렉터리 clone·push와 기존 폴더 pull
  - README 절차의 macOS 최종 재현 로그
  - 전체 제출물 최종 비밀값 점검
- 제한 시간 기능은 사용자가 직접 확인했지만 해당 화면의 원본 로그나 캡처는 아직
  `evidence/`에 없다.

### 병합 준비 상태와 권장 명령

- 기능상 `main` 병합을 막는 문제는 발견하지 못했다.
- 이번 점검 문서 변경의 권장 커밋 메시지:
  `Docs: 제한 시간 기능 검증과 병합 준비 정리`
- 문서 커밋과 push 후 다음 명령으로 병합 커밋을 명시적으로 남긴다.

```zsh
git checkout main
git pull --ff-only origin main
git merge --no-ff Test/time-limit -m "Merge: 제한 시간 기능 브랜치 병합"
git push origin main
git status --short --branch
git log --oneline --graph --decorate --all -15
```

- `--no-ff`를 사용하므로 fast-forward가 가능해도 별도 merge commit이 남는다.
- 실제 commit, merge와 push는 이번 점검에서 수행하지 않았다.

---

## 2026-08-06 — 제한 시간 브랜치 병합 후 증거와 최종 순서 정리

- 환경: macOS / zsh / Python 3.12.13 / Git 2.53.0
- 브랜치: `main`
- 목표: 사용자 병합 결과, 현재 실행 화면과 무작위 출제를 확인하고 남은 필수
  작업의 수행 순서를 최신화한다.

### Git과 현재 화면 확인

- 사용자가 제공한 `git log --oneline --graph --all -30`에서 다음을 확인했다.
  - `cf18374 (HEAD -> main, origin/main) Merge: 제한 시간 기능 브랜치 병합`
  - `34502ed Docs: 제한 시간 기능 검증 정리`
  - `ddc2d8e Fix: 힌트와 오류 메시지 출력 위치 안정화`
  - `e53b9cf Feat: 제한 시간과 자동 힌트 기능 실험`
- `evidence/screenshots/main-menu.png`에서 병합 후 메뉴 1~6을 확인했다.
- `evidence/screenshots/game-play.png`에서 5문제 선택, 자동 힌트, 카운트다운과
  힌트 후 정답 1점 동작을 확인했다.
- 세부 메뉴마다 화면을 모두 추가하지 않고 평가 시 기능 체크리스트를 따라 실제
  실행한다. 다만 체크리스트는 미션에 명시된 핵심 실행 증거를 대체하지 않으므로,
  추가·목록·플레이 결과·점수·재실행 화면은 남은 증거로 유지한다.

### 무작위 출제 확인

- `src/game_manager.py`의 `play_quizzes()`는 다음 호출로 문제를 선택한다.

```python
selected_quizzes = random.sample(self.quizzes, k=quiz_count)
```

- 코드에는 `random.seed()`나 저장된 출제 순서가 없다.
- 기본 문제 5개를 모두 선택하는 독립 Python 실행을 8회 반복했고 7가지 서로 다른
  순서가 나왔다. 따라서 전체 5문제를 선택해도 출제 순서는 매 게임 무작위다.
- 현재 플레이 화면에서도 JSON의 첫 문제인 물의 화학식이 아니라 태양계 행성 문제가
  먼저 나와 실제 순서 변경을 확인할 수 있다.
- 5개 전체의 특정 순서가 바로 다음 실행에서 우연히 같을 확률은 `1 / 5!`, 즉
  `1/120`이다.

### 문서와 다음 작업

- README, 요구사항 추적표, 진행 상태와 아키텍처 계획을 `cf18374` 기준으로 갱신했다.
- 현재 메뉴·플레이 화면은 확보로 표시하고, 나머지 기능은 평가용 체크리스트 확인과
  미션 핵심 증거 대상으로 남겼다.
- clone·pull은 이후 커밋 때문에 이력이 혼동되지 않도록 모든 내용·문서·증거 커밋이
  끝난 뒤 마지막 Git 실습으로 수행한다.
- 다음 작업은 평가용 체크리스트 작성과 추가·점수 영속성 최종 확인이다. 이후 최종
  Git 그래프를 확보하고 마지막으로 clone·push·pull 실습을 진행한다.

---
