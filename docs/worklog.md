# 작업 기록

실제 수행한 내용만 날짜별로 기록한다. 실행하지 않은 명령과 예상 결과는 기록하지 않는다.

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
