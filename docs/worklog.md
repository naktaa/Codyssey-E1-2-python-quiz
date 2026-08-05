# 작업 기록

실제 수행한 내용만 날짜별로 기록한다. 실행하지 않은 명령과 예상 결과는 기록하지 않는다.

## 현재 기록 원칙

- 2026-08-05 이후 unittest는 실행하거나 수정하지 않는다.
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
- `tests/test_game_manager.py`: 메뉴·입력·종료 자동 테스트 4개 추가
- `README.md`: 메뉴와 공통 입력의 검증 상태 반영
- `docs/requirements.md`: 실제 구현·검증 상태 반영
- `docs/progress.md`: 현재 단계와 다음 작업 갱신
- `docs/troubleshooting.md`: 실제 테스트·컴파일 실패와 해결 기록

### 실행 명령과 실제 결과

```zsh
python3 -m unittest discover -s tests -v
env PYTHONPYCACHEPREFIX=/private/tmp/codyssey-e1-2-pycache python3 -m compileall -q .
printf '1\n5\n' | python3 main.py
```

- 결과: 성공
- 실제 출력 요약: 메뉴와 공통 입력 자동 테스트 4개가 모두 통과했다.
- 실제 출력 요약: 임시 bytecode 캐시 경로를 사용한 전체 Python 컴파일이
  출력 없이 성공했다.
- 실제 출력 요약: 메뉴 1번 선택 시 미구현 안내 후 메뉴로 돌아오고 5번
  선택 시 traceback 없이 종료했다.
- 실제 출력 요약: `src.game_manager`에서 `QuizGame`을 import하는 구조로 옮긴
  뒤에도 자동 테스트 4개와 실제 실행이 동일하게 통과했다.

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
- `tests/test_quiz.py`: 정상·오류 데이터와 변환 동작 테스트 8개 작성
- `README.md`, `docs/architecture-plan.md`: 실행 명령을 Python 3.12.13의
  `python` 기준으로 정리

### 실행 명령과 실제 결과

```zsh
python --version
```

- 결과: 성공
- 실제 출력: `Python 3.12.13`
- 확인 필요: 최종 코드의 `python -m unittest discover -s tests -v` 결과는
  사용자 터미널에서 확인 후 실행 검증 완료로 변경한다.

### 증거

- 새 스크린샷 없음
- Quiz 데이터 모델은 최종 자동 검증 로그로 증명 예정

### Git 상태

- 커밋: `6e55f31 Feat: 퀴즈 클래스 기본 구현`
- push: `origin/main`에 완료

### 다음 작업

- Python 3.12.13 자동 테스트 통과 후 `feature/solving` 브랜치를 생성한다.

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
- `tests/test_game_manager.py`: 카테고리 중복 제거, 빈 목록과 선택 출제 테스트 추가
- `tests/test_quiz.py`: 임시 기본 데이터가 새 객체 목록을 반환하는지 검증
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
- 확인 필요: 사용자 Python 3.12.13 환경에서 전체 `unittest` 실행

### 증거

- 브랜치 생성 터미널 로그를 작업 기록에 반영
- 실제 문제를 추가한 뒤 `evidence/screenshots/play-result.png` 확보 예정

### Git 상태

- 커밋: `65312c4 Feat: 퀴즈 풀기 기능 기본 구현`
- push: `origin/feature/solving`에 완료
- `main` 병합: `cb4f9cb Merge: 퀴즈 플레이 브랜치 병합`

### 다음 작업

- Python 3.12.13 자동 테스트와 직접 플레이 흐름을 확인한다.

---

## 2026-08-04 — main 메모리 기반 퀴즈 추가 구현

- 환경: macOS / zsh / Python 3.12.13 사용자 환경
- 브랜치: `main`
- 목표: JSON 저장 없이 퀴즈 등록 입력과 같은 실행 내 사용을 먼저 검증
- 요구사항: `FUNC-09`, `FUNC-10`

### 변경 파일

- `src/game_manager.py`: 카테고리 이름, 문제, 선택지 4개와 정답을 입력해 메모리 목록에 추가
- `tests/test_game_manager.py`: 오류 입력과 직접 입력한 카테고리의 메모리 추가 테스트
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
- 빈 카테고리·문제·선택지 재입력은 자동 테스트로 확인했다.
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
PYTHONPYCACHEPREFIX=/private/tmp/codyssey-e1-2-audit-pycache python -m unittest discover -s tests -v
PYTHONPYCACHEPREFIX=/private/tmp/codyssey-e1-2-audit-pycache python -m compileall -q .
git diff --check
printf '2\n문화\n대한민국의 수도는?\n서울\n부산\n인천\n대전\n1\n1\n3\n1\n5\n' | python main.py
python main.py < /dev/null
```

- 자동 테스트 17개가 모두 통과했다.
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
- 자동 테스트 파일은 사용자 요청에 따라 수정하거나 다시 실행하지 않았다.

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
- 자동 테스트 파일은 사용자 요청에 따라 수정하거나 실행하지 않았다.
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
- 자동 테스트 파일은 사용자 요청에 따라 수정하거나 실행하지 않았다.
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
- 이 `test`는 unittest가 아니라 사용자가 `main.py`를 직접 실행할 때 데이터
  파일만 분리하는 확인용 모드다.
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

- 2026-08-05 이후 unittest를 실행·수정하지 않는 원칙을 명시했다.
- 과거 unittest 기록은 삭제하지 않고 당시 이력으로만 유지한다.
- 사용자 제공 로그의 콘솔 내용은 다시 가공하지 않고 원형 중심으로 보존한다.
- 구현 완료, 사용자 직접 확인, 증거 확보, 미검증을 분리해 표시한다.
- 실제·확인용 데이터와 JSON 적용 전·후 영속성을 구분한다.
- 메뉴와 Git 화면의 기존 자료는 개발 과정 증거로 두고 최종본은 모든 기능과
  병합이 끝난 뒤 다시 정리한다.
- 계정명과 호스트명은 이후 사용자 지시에 따라 별도 마스킹·재촬영 조건으로
  보지 않는다. 토큰·키·인증정보 같은 비밀값은 계속 기록하지 않는다.

### 변경 파일

- `AGENTS.md`: 앞으로 unittest를 실행·수정하지 않는 작업 원칙 추가
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
- unittest는 정책에 따라 실행하거나 수정하지 않았다.

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
- unittest는 실행하거나 수정하지 않았다.

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
- unittest는 실행하거나 수정하지 않았다.
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
- unittest는 실행하거나 수정하지 않았다.
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
- unittest는 실행하거나 수정하지 않았다.
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
- unittest는 실행하거나 수정하지 않는다.

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
- unittest는 실행하거나 수정하지 않는다.

### Git 상태

- Git 명령은 사용자 지시에 따라 실행하지 않음
- commit·push: 사용자 직접 수행

### 다음 작업

- 날짜와 시간을 포함하는 점수 기록 히스토리의 저장 구조와 표시 방식을 설계한다.

---

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
- unittest는 실행하거나 수정하지 않는다.

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
- 삭제 기능의 정상 동작은 사용자가 직접 확인했다.
- unittest는 실행하거나 수정하지 않는다.

### Git 상태

- Git 명령은 사용자 지시에 따라 실행하지 않음
- commit·push: 사용자 직접 수행

### 다음 작업

- 날짜와 시간을 포함하는 점수 기록 히스토리의 저장 구조와 표시 방식을 설계한다.
