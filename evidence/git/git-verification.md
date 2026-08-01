# 초기 Git 저장소 설정 검증

- 수행일: 2026-08-01
- 환경: macOS / zsh / Python 3.12.13 / Git 2.53.0
- 저장소: `https://github.com/naktaa/Codyssey-E1-2-python-quiz.git`

## 환경 확인

```zsh
python3 --version
git --version
```

```text
Python 3.12.13
git version 2.53.0
```

## 저장소 초기화

```zsh
git init -b main
git status --short --branch
```

```text
빈 Git 저장소를 다시 초기화했습니다.
## 아직 커밋이 없습니다, 위치: <main
?? .gitattributes
?? .gitignore
?? AGENTS.md
?? MISSION.md
?? README.md
?? docs/
?? evidence/
```

## 첫 커밋

```zsh
git add .
git commit -m "Chore: 프로젝트 초기 파일 구성"
```

```text
[main (최상위-커밋) a4887e4] Chore: 프로젝트 초기 파일 구성
12 files changed, 736 insertions(+)
```

커밋은 성공했지만 Git이 사용자 이름과 이메일을 시스템 정보에서 자동으로
추정했다는 경고가 표시됐다. 다음 커밋 전에 저장소 로컬 사용자 설정을 명시적으로
확인해야 한다.

## 원격 저장소 연결과 push

```zsh
git remote add origin https://github.com/naktaa/Codyssey-E1-2-python-quiz.git
git push -u origin main
```

```text
To https://github.com/naktaa/Codyssey-E1-2-python-quiz.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

## 최종 상태 확인

```zsh
git log -1 --oneline --decorate
git status --short --branch
```

```text
a4887e4 (HEAD -> main, origin/main) Chore: 프로젝트 초기 파일 구성
## main...origin/main
```

로컬 `main`과 `origin/main`이 같은 첫 커밋을 가리키며 작업 트리는 깨끗한
상태였다. 이후 증거 파일과 문서 기록을 추가하면서 새 변경사항이 생겼다.

## 화면 증거

- [Python·Git 버전과 첫 커밋 상태](git-log.png)

공개 전 화면에 표시된 로컬 계정명과 호스트명이 공개 가능한 정보인지 최종
보안 점검에서 다시 확인한다.
