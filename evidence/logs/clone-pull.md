# clone·push·pull 사용 기록

- 확인일: 2026-08-09
- 확인 위치: 현재 macOS 작업 저장소의 로컬 reflog
- 목적: 집과 강의장 환경을 오가며 실제 수행한 clone·push·pull 흐름을 보존한다.

Git reflog는 원격 저장소에 push되지 않는 로컬 기록이므로 아래 실제 출력을 문서로
남겼다.

## clone과 pull

실행 명령:

```zsh
git reflog show HEAD --date=iso | rg 'clone:|pull .*Fast-forward'
```

실제 출력:

```text
e22a61a HEAD@{2026-08-09 15:24:01 +0900}: pull --tags origin main: Fast-forward
c362ed7 HEAD@{2026-08-06 15:09:32 +0900}: pull --tags origin main: Fast-forward
b8d5a28 HEAD@{2026-08-05 15:12:56 +0900}: clone: from https://github.com/naktaa/Codyssey-E1-2-python-quiz.git
```

## push와 원격 변경 반영

실행 명령:

```zsh
git reflog show origin/main --date=iso | rg 'update by push|fetch: fast-forward'
```

확인에 사용한 최신 출력:

```text
9403a8a refs/remotes/origin/main@{2026-08-09 16:33:04 +0900}: update by push
9d76c98 refs/remotes/origin/main@{2026-08-09 16:25:46 +0900}: update by push
e22a61a refs/remotes/origin/main@{2026-08-09 15:23:49 +0900}: fetch: fast-forward
9485d5f refs/remotes/origin/main@{2026-08-06 19:16:40 +0900}: update by push
cf18374 refs/remotes/origin/main@{2026-08-06 18:11:01 +0900}: update by push
ba58b00 refs/remotes/origin/main@{2026-08-06 16:31:53 +0900}: update by push
8f5b8b7 refs/remotes/origin/main@{2026-08-06 16:25:07 +0900}: update by push
a624524 refs/remotes/origin/main@{2026-08-06 15:44:25 +0900}: update by push
```

## 판정

- GitHub 저장소에서 현재 작업 폴더를 clone한 기록이 있다.
- 다른 환경에서 반영된 원격 커밋을 현재 폴더에서 Fast-forward pull한 기록이 두 번
  있다.
- 현재 폴더에서 원격 `main`으로 push한 기록도 여러 번 있다.
- 따라서 별도의 세 번째 컴퓨터에서 같은 실습을 반복하지 않고 기존 두 환경의 실제
  이력을 clone·push·pull 사용 증거로 사용한다.
