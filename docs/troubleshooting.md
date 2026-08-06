# 트러블슈팅 기록

실제로 발생하고 해결한 오류만 기록한다. 예상 오류나 가상의 해결 사례는 추가하지 않는다.

## 기록 형식

### YYYY-MM-DD — 문제 제목

- 관련 요구사항: `ID`
- 환경: macOS / zsh / Python 버전
- 실패 명령 또는 동작:

```zsh
실제로 실패한 명령
```

- 증상: 오류 메시지와 사용자에게 보인 동작
- 원인: 확인된 원인
- 해결: 실제 적용한 변경
- 재검증 명령:

```zsh
실제로 다시 실행한 명령
```

- 재검증 결과: 성공 / 실패
- 관련 변경 파일:
- 관련 커밋:
- 재발 방지:

---

## 현재 기록

## 2026-08-06 — 카운트다운이 문제와 선택지를 덮어쓰는 오류

- 관련 요구사항: `BONUS-06`, `BONUS-07`
- 환경: macOS 터미널 / zsh
- 실패 동작: 제한 시간 퀴즈를 실행하고 매초 카운트다운 갱신을 기다림
- 증상: 타이머가 갱신될 때마다 위쪽으로 이동해 문제와 선택지를 지우고, 이전
  타이머 출력이 여러 줄에 남았다.
- 원인: 타이머 줄을 바꾸기 위해 ANSI 커서 저장·복원과 위쪽 이동을 사용했고,
  실제 터미널에서 커서가 원래 입력 줄로 복원되지 않으면 다음 갱신이 현재 위치를
  기준으로 다시 위로 이동했다.
- 해결: 위쪽 커서 이동을 제거하고 현재 입력 줄에 `남은 시간 | 정답 번호`를
  함께 표시했다. 비정규·비에코 입력 모드에서 입력 문자를 내부 버퍼로 관리해
  현재 줄을 다시 그려도 입력 내용이 유지되도록 했다.
- 재검증 명령:

```zsh
python3 -m py_compile main.py src/*.py
python3 -m json.tool state.json >/dev/null
git diff --check
```

- 재검증 결과: 정적 검사 성공. PTY 검사에서 빠른 정답, 자동 힌트, 잘못된 입력,
  시간 초과 입력 분리와 `KeyboardInterrupt`가 통과했고 커서 위 이동·저장
  시퀀스가 출력되지 않음을 확인했다. 실제 터미널 화면은 사용자 재확인 필요.
- 관련 변경 파일: `src/timed_input.py`, `README.md`, `docs/architecture-plan.md`,
  `docs/progress.md`, `docs/requirements.md`, `docs/worklog.md`,
  `docs/troubleshooting.md`
- 관련 커밋: 미커밋
- 재발 방지: 동적 터미널 출력은 위쪽 고정 행의 커서 상태를 가정하지 않고 현재
  입력 줄 안에서만 갱신하며, 실제 터미널 화면을 최종 확인한다.

---

## 2026-08-04 — macOS Python bytecode 캐시 쓰기 권한 오류

- 관련 요구사항: `ENV-01`
- 환경: macOS / zsh / Python 3.12.13
- 실패 명령 또는 동작:

```zsh
python3 -m compileall -q .
```

- 증상: 사용자 라이브러리 아래 기본 캐시 경로에 대한 `PermissionError`로
  프로젝트 Python 파일 컴파일이 실패했다.
- 원인: 현재 실행 환경에서 macOS Python의 기본 bytecode 캐시 경로에 쓰기
  권한이 없었다.
- 해결: 프로젝트 파일을 바꾸지 않고 `PYTHONPYCACHEPREFIX`를 `/private/tmp`
  아래 전용 경로로 지정했다.
- 재검증 명령:

```zsh
env PYTHONPYCACHEPREFIX=/private/tmp/codyssey-e1-2-pycache python3 -m compileall -q .
```

- 재검증 결과: 성공, 출력 없이 종료 코드 0
- 관련 변경 파일: 없음
- 관련 커밋: 해당 없음
- 재발 방지: 현재 검증 환경에서 `compileall` 실행 시 동일한 임시 캐시 경로를
  사용한다.

---

## 2026-08-05 — 입력 스트림 종료 시 EOFError traceback

- 관련 요구사항: `FUNC-04`
- 환경: macOS / zsh / Python 3.12.13
- 실패 명령 또는 동작:

```zsh
python main.py < /dev/null
```

- 증상: 메뉴 입력에서 `EOFError` traceback이 발생하고 종료 코드 1로 끝났다.
- 원인: 입력 중단 예외를 처리하는 코드가 메뉴 실행 흐름에 없었다.
- 해결: `run()` 전체에서 `EOFError`와 `KeyboardInterrupt`를 잡고
  `safe_exit()`로 종료 안내를 출력하도록 변경했다.
- 재검증 명령:

```zsh
python main.py < /dev/null
python main.py
# 입력 대기 중 Ctrl+C
```

- 재검증 결과: 성공, 두 경우 모두 traceback 없이 종료 코드 0
- 관련 변경 파일: `src/game_manager.py`
- 관련 커밋: `49f97b5 Fix: 입력 중단 시 안전 종료 처리`
- 재발 방지: 새 입력 기능은 `run()`이 관리하는 실행 흐름 안에서 호출한다.

---

## 2026-08-05 — 확인용 JSON의 필수 키 이름 오류

- 관련 요구사항: `DATA-05`, `DATA-06`
- 환경: macOS / zsh / Python 3.12.13
- 실패 명령 또는 동작:

```zsh
QUIZ_STATE_MODE=test py
```

- 증상: 확인용 `state.test.json`의 최상위 키가 `quizzes`가 아니라 `quizes`로
  기록되어 `상태 파일이 손상되었습니다: quizzes는 목록이어야 합니다.`가 출력됐다.
- 원인: `validate_state_data()`가 필수 `quizzes` 값을 찾지 못해 `None`을 받고,
  목록 형식 검증에서 `ValueError`를 발생시켰다.
- 해결: `load_state()`가 스키마 오류를 잡아 `recover_corrupted_state()`를 호출하고,
  `backup_corrupted_state()`가 손상 원본을 먼저 복사한 뒤 기본 상태 파일을 만들도록
  구현했다.
- 재검증 결과: 성공, traceback 없이 메뉴가 실행됐다.
- 생성 백업:
  `state.test.json.corrupt-20260805-181939-287895`
- 백업 내용: 정상 데이터와 동일한 퀴즈 4개를 포함하지만 최상위 키가
  `"quizes"`로 잘못 기록된 손상 원본
- 관련 증거: [복구 연결 기록](../evidence/logs/json-recovery.md),
  [터미널 캡처](../evidence/screenshots/json-recovery.png)
- 관련 변경 파일: `src/game_manager.py`, `.gitignore`,
  `evidence/screenshots/json-recovery.png`
- 관련 커밋: `103a3b1 Fix: 손상된 상태 파일 백업과 복구 처리`
- 재발 방지: 상태 데이터를 객체로 사용하기 전에 `validate_state_data()`에서
  최상위 구조와 각 필드 형식을 검증하고, 손상 원본은 복구 전에 별도 백업한다.

---

## 2026-08-06 — 추적 중인 state.json의 히스토리 필드 누락

- 관련 요구사항: `BONUS-05`, `DATA-02`
- 환경: Linux / bash / Python 3.12.3 격리 복사본
- 확인 동작: `state.json` 내용과 히스토리 구현 커밋 `4da450f` 비교
- 증상: 코드와 README는 `score_history`를 사용하지만 Git에 추적된
  `state.json`에는 해당 필드가 없었다.
- 원인: 히스토리 구현 시 기존 JSON에 필드가 없어도 빈 목록으로 읽는 호환 코드는
  추가했지만, 저장소의 기본 `state.json` 자체는 갱신하지 않았다.
- 해결: `state.json`에 `"score_history": []`를 추가하고 기존 파일 호환 처리는
  그대로 유지했다.
- 재검증 명령:

```bash
python3 -m json.tool state.json
python3 -m compileall -q main.py src
```

- 재검증 결과: JSON·Python 문법 확인 성공, 격리 복사본에서 플레이 기록 저장과
  재실행 복원 성공
- 관련 변경 파일: `state.json`, `src/game_manager.py`, `README.md`
- 관련 커밋: `81dddf1 Refactor: 테스트 기록 정리와 점수·히스토리 표시 개선`
- 재발 방지: JSON 스키마 필드를 추가할 때 불러오기 호환 코드와 저장소의 기본
  상태 파일을 함께 대조한다.
