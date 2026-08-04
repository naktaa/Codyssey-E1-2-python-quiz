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

- 커밋 메시지: `Docs: 상식 퀴즈 구현 계획 정리`
- push: 미실시

### 다음 작업

- 메뉴 1~5와 공통 입력 처리를 담당하는 최소 `QuizGame` 골격을 구현한다.
