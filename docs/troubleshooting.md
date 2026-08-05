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

## 2026-08-04 — 메뉴 제목 테스트 문자열 불일치

- 관련 요구사항: `FUNC-01`
- 환경: macOS / zsh / Python 3.12.13
- 실패 명령 또는 동작:

```zsh
python3 -m unittest discover -s tests -v
```

- 증상: 메뉴 제목 테스트 1개가 실패하고 나머지 3개는 통과했다.
- 원인: 실제 제목 문자열 앞에 줄바꿈 문자가 포함되어 정확한 문자열 비교와
  일치하지 않았다.
- 해결: 빈 줄과 메뉴 제목을 별도 출력으로 분리해 각 출력의 의미를 명확히 했다.
- 재검증 명령:

```zsh
python3 -m unittest discover -s tests -v
```

- 재검증 결과: 성공, 테스트 4개 통과
- 관련 변경 파일: `src/game_manager.py`, `tests/test_game_manager.py`
- 관련 커밋: `3b3914c`
- 재발 방지: 출력 함수에 전달되는 한 항목이 한 줄의 의미만 갖도록 구성한다.

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
- 관련 커밋: 미커밋
- 재발 방지: 새 입력 기능은 `run()`이 관리하는 실행 흐름 안에서 호출한다.
