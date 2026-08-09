# 상식 퀴즈 게임 아키텍처

## 문서 목적

현재 코드의 객체별 책임, 주요 동작과 데이터 저장 기준을 기록한다. 동료평가에 필요한
간단한 설명은 `README.md`에 두고, 이 문서는 구조를 변경할 때 확인하는 구현 기준으로
사용한다.

## 설계 원칙

- `Quiz`는 퀴즈 한 문제의 데이터와 규칙을 담당한다.
- `GameManager`는 메뉴와 게임 진행을 담당한다.
- `StateManager`는 파일 상태의 저장·검증·복구를 담당한다.
- `TimedTerminalInput`은 제한 시간이 있는 터미널 답 입력을 담당한다.
- `main.py`는 객체를 조립하고 실행만 시작한다.
- 실제 데이터와 테스트 데이터는 상태 파일 경로로 분리한다.
- 외부 라이브러리를 사용하지 않고 Python 표준 라이브러리만 사용한다.

한 클래스가 게임 흐름과 JSON 복구를 동시에 처리하지 않도록 역할을 분리한다. 현재
규모에서는 별도 인터페이스나 저장소 계층을 추가하지 않고, `StateManager` 객체를
`GameManager`에 전달하는 단순한 합성 구조를 사용한다.

## 전체 구조

```text
main.py
  ├── --test 옵션으로 상태 경로 선택
  ├── StateManager
  └── GameManager
        ├── list[Quiz]
        ├── best_score
        ├── score_history
        ├── TimedTerminalInput
        └── StateManager
              ├── state.json 또는 state.test.json
              └── 파일 없음·손상 시 기본 Quiz 생성
```

## 객체별 책임

### `Quiz`

파일: `src/quiz.py`

```python
Quiz(
    question: str,
    choices: list[str],
    answer: int,
    hint: str,
)
```

- 문제, 선택지 4개, 정답 번호와 힌트 보관
- 필수 문자열의 공백 정리와 빈 값 검증
- 선택지 개수와 정답 범위 검증
- 문제와 선택지 출력
- 사용자 답의 정오답 확인
- `to_dict()`와 `from_dict()`를 통한 JSON 변환

### `StateManager`

파일: `src/state_manager.py`

- 파일이 없거나 손상됐을 때만 기본 상태 생성
- UTF-8 JSON 저장과 불러오기
- 임시 파일 작성 후 활성 파일 교체
- 퀴즈, 최고 점수와 플레이 기록 스키마 검증
- 손상된 원본 백업과 기본 상태 복구
- 원본 보호가 필요한 경우 해당 실행의 저장 비활성화

`StateManager.save_state()`는 퀴즈, 최고 점수와 플레이 기록을 직접 전달받는다.
`load_state()`는 같은 세 값을 튜플로 반환한다. 파일이 없으면 기본 상태를 만들어
저장하고, 읽기 오류나 백업 실패가 있으면 기본 상태로 실행한다.

### `GameManager`

파일: `src/game_manager.py`

- 메뉴 표시와 번호별 메서드 딕셔너리 디스패치
- 정수, 필수 문자열과 `y/n` 입력 검증
- 풀 문제 수 선택과 무작위 출제
- 퀴즈 추가·목록·삭제
- 최고 점수 비교와 플레이 기록 관리
- 정상 종료와 입력 중단 종료
- 현재 퀴즈, 최고 점수와 플레이 기록을 `StateManager`에 저장 위임
- 불러온 퀴즈, 최고 점수와 플레이 기록을 현재 게임 상태에 반영

`save_state()`와 `load_state()`는 미션에서 저장 책임을 찾기 쉽도록 `GameManager`에도
유지한다. 두 메서드는 파일을 직접 처리하지 않고 `StateManager`를 호출한다.

추가·삭제·플레이 기록 저장이 실패하면 `GameManager`가 변경 전 메모리 상태로
되돌린다. 파일 처리 성공 여부는 `StateManager`, 게임 변경 롤백은 `GameManager`가
담당하는 경계다.

### `TimedTerminalInput`

파일: `src/timed_input.py`

- `select.select()`와 `time.monotonic()`을 사용한 10초 제한 시간
- 1초 단위 카운트다운
- 5초 후 자동 힌트 공개
- 입력 중인 문자열 유지와 잘못된 답 재입력
- 시간 초과 입력이 다음 문제로 넘어가지 않도록 입력 큐 정리
- TTY가 아닌 입력의 줄 단위 처리

macOS 터미널을 최종 실행 기준으로 사용한다. 제한 시간 입력은 일반 메뉴 입력과
동작 방식이 다르므로 `GameManager.read_int()`와 분리한다.

### `main.py`

- 실행 모드에 맞는 상태 경로 선택
- `StateManager` 생성
- `GameManager`에 `StateManager` 전달
- 상태 불러오기 후 게임 실행

## 주요 기능 흐름

### 프로그램 시작

```text
main.py
  → 상태 파일 경로 선택
  → StateManager 생성
  → 파일 없음·손상 시에만 기본 퀴즈 생성
  → GameManager 생성
  → GameManager.load_state()
  → StateManager.load_state()
  → GameManager.run()
```

### 퀴즈 추가·삭제

1. `GameManager`가 입력을 검증한다.
2. 메모리의 퀴즈 목록을 변경한다.
3. 퀴즈 목록, 최고 점수와 플레이 기록으로 `StateManager.save_state()`를 호출한다.
4. 저장 성공 시 변경을 확정한다.
5. 저장 실패 시 메모리 목록과 필요한 점수 상태를 되돌린다.

### 퀴즈 플레이

1. 전체 문제 수 안에서 풀 문제 수를 선택한다.
2. `random.sample()`로 원본 목록을 변경하지 않고 출제 목록을 만든다.
3. 문제마다 `TimedTerminalInput`이 답, 시간 초과와 힌트 공개 여부를 반환한다.
4. 정답이면 현재 점수에 3점을 더하고, 힌트가 공개된 정답이면 2점을 차감한다.
5. 오답과 시간 초과는 점수를 변경하지 않고 각 문제 뒤에 현재 누적 점수를 표시한다.
6. 최종 점수를 기존 최고 점수와 비교한다.
7. 플레이 기록과 최고 점수를 한 번에 저장한다.
8. 저장 실패 시 새 기록과 최고 점수 변경을 되돌린다.

## 점수 정책

- 최고 점수는 문제 수로 정규화하지 않고 실제 획득 점수만 비교한다.
- 문제 수가 많을수록 획득 가능한 최대 점수가 높다.
- 높은 최고 점수를 목표로 할 때 많은 문제를 선택하도록 유도하는 의도된 정책이다.
- 플레이 기록에는 플레이 시각과 획득 점수만 저장한다.

## 상태 파일

- 실제 실행: 프로젝트 루트의 `state.json`
- 테스트 실행: 프로젝트 루트의 `state.test.json`
- 테스트 실행 옵션: `python3 main.py --test`
- 인코딩: UTF-8
- JSON 출력: `ensure_ascii=False`, 들여쓰기 4칸
- 손상 백업: `상태파일명.corrupt-YYYYMMDD-HHMMSS[-순번]`

```json
{
  "quizzes": [],
  "best_score": null,
  "score_history": [
    {
      "played_at": "2026-08-09 15:30",
      "score": 7
    }
  ]
}
```

상태 파일이 없으면 기본 퀴즈 5개와 빈 점수로 새 파일을 만든다. JSON 문법 또는
스키마가 손상되면 원본을 백업한 뒤 기본 상태를 저장한다. 백업에 실패하면 손상
원본을 덮어쓰지 않도록 해당 실행의 저장을 중지한다.

## 안전 종료

- 메뉴 종료, `KeyboardInterrupt`, `EOFError`는 `GameManager.safe_exit()`으로 모은다.
- 종료 시 현재 상태 저장을 시도한다.
- 입력 중단은 traceback 없이 안내하고 종료한다.
- 저장 실패는 사용자에게 안내하며 메모리와 파일의 불일치를 가능한 범위에서 막는다.

## 검증 기준

- Python 파일 구문과 import 성공
- 파일 없음 → 기본 상태 생성 → 재로드
- 퀴즈 추가·삭제 → 저장 → 재로드
- 플레이 → 최고 점수·기록 저장 → 재로드
- 손상 JSON → 원본 백업 → 기본 상태 복구
- 저장 실패 → 추가·삭제·기록 변경 롤백
- EOF와 `Ctrl+C` 안전 종료
- macOS 터미널에서 제한 시간·자동 힌트 최종 확인

실제 검증 상태와 남은 증거는 `docs/requirements.md`와 `docs/progress.md`에서
관리하고, 실행 명령과 결과는 `docs/worklog.md`에 기록한다.
