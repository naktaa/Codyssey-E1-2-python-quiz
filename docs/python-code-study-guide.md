# 퀴즈 게임으로 공부하는 Python 코드 흐름

## 문서 목적

이 문서는 E1-2 퀴즈 게임의 실제 실행 순서를 따라가면서 Python 문법과 표준
라이브러리를 함께 학습하기 위한 자료다.

문법을 사전처럼 따로 외우기보다 다음 질문을 중심으로 코드를 읽는다.

- 프로그램이 실행되면 가장 먼저 어떤 코드가 동작하는가?
- 각 함수와 클래스는 어떤 값을 받고 무엇을 반환하는가?
- 해당 문법이나 표준 라이브러리가 이 위치에서 왜 필요한가?
- 파일이 없거나 입력과 저장에 실패하면 어떤 흐름으로 이동하는가?

이 문서는 현재 단순화된 코드 구조를 기준으로 한다. 이전 버전에 있던 환경 변수
방식, 이전 JSON 스키마 이전, 누락 힌트 복원과 세부 플레이 통계는 다루지 않는다.

## 전체 실행 흐름

```text
python3 main.py 실행
  → argparse로 --test 옵션 확인
  → Path로 사용할 상태 파일 경로 선택
  → StateManager와 GameManager 객체 생성
  → JSON 상태 불러오기와 검증
  → 파일이 없거나 손상됐을 때만 기본 Quiz 객체 5개 생성
  → 메뉴 반복
  → 선택한 기능 실행
  → 변경된 경우 JSON 저장
  → 종료 또는 입력 중단 시 최종 저장
```

실제 데이터를 변경하지 않고 학습할 때는 프로젝트 루트에서 다음 명령을 사용한다.

```zsh
python3 main.py --test
```

---

## 1. `main.py`: 프로그램 시작점

관련 코드: [`main.py`](../main.py)

```python
import argparse

from src.game_manager import GameManager
from src.state_manager import DEFAULT_STATE_PATH, TEST_STATE_PATH, StateManager
```

### `import`가 하는 일

`import`는 다른 모듈에 있는 기능을 현재 파일에서 사용할 수 있게 가져온다.

```python
import argparse
```

`argparse`는 Python을 설치하면 함께 제공되는 표준 라이브러리다. 별도의 패키지
설치가 필요하지 않다.

```python
from src.game_manager import GameManager
```

프로젝트의 `src/game_manager.py` 모듈에서 `GameManager` 클래스만 가져온다.

현재 프로젝트의 import는 두 종류로 구분할 수 있다.

| 종류 | 예 | 의미 |
|---|---|---|
| 표준 라이브러리 | `argparse`, `json`, `random`, `pathlib` | Python이 기본 제공 |
| 프로젝트 모듈 | `src.quiz`, `src.game_manager` | 직접 작성한 코드 |

### `main()` 함수

```python
def main() -> None:
    ...
```

- `def`: 함수 정의
- `main`: 함수 이름
- `()`: 호출할 때 반드시 전달할 매개변수가 없음
- `-> None`: 특별한 결과값을 반환하지 않는다는 타입 힌트
- `:` 다음의 들여쓰기: 함수에 포함된 코드

`main()`은 퀴즈 기능을 직접 구현하지 않는다. 필요한 객체를 만들고 다음 실행
순서를 연결하는 역할을 한다.

```python
state_path = TEST_STATE_PATH if args.test else DEFAULT_STATE_PATH
state_manager = StateManager(state_path)
game_manager = GameManager(state_manager)
game_manager.load_state()
game_manager.run()
```

### 프로그램 진입 조건

```python
if __name__ == "__main__":
    main()
```

Python 파일을 직접 실행하면 해당 파일의 `__name__` 값은 `"__main__"`이 된다.

```zsh
python3 main.py
```

따라서 위 명령에서는 `main()`이 실행된다. 반면 다른 Python 파일이 `main.py`를
단순히 import하면 `main()`이 자동 실행되지 않는다.

### 학습 확인

- `main()`은 왜 퀴즈 문제를 직접 출력하지 않는가?
- `if __name__ == "__main__"`을 제거하면 import할 때 어떤 차이가 생기는가?

---

## 2. `argparse`: 실행 옵션 처리

```python
parser = argparse.ArgumentParser(description="터미널 상식 퀴즈 게임")
parser.add_argument(
    "--test",
    action="store_true",
    help="실제 데이터 대신 state.test.json을 사용합니다.",
)
args = parser.parse_args()
```

### `ArgumentParser`

명령어에 전달된 옵션을 분석하는 객체다.

```zsh
python3 main.py --test
```

여기서 `--test`가 명령어 옵션이다.

### `add_argument()`

```python
parser.add_argument("--test", action="store_true")
```

`--test` 옵션을 프로그램에 등록한다. `action="store_true"`는 옵션 유무를
`bool` 값으로 바꾼다.

| 실행 명령 | `args.test` |
|---|---:|
| `python3 main.py` | `False` |
| `python3 main.py --test` | `True` |

`bool`은 `True`와 `False` 두 값만 갖는 자료형이다.

### 조건 표현식

```python
state_path = TEST_STATE_PATH if args.test else DEFAULT_STATE_PATH
```

일반 조건문으로 풀면 다음과 같다.

```python
if args.test:
    state_path = TEST_STATE_PATH
else:
    state_path = DEFAULT_STATE_PATH
```

### 왜 `argparse`를 사용했는가?

- 실제 데이터와 학습용 데이터를 명확하게 분리한다.
- `sys.argv` 문자열을 직접 분석하지 않아도 된다.
- `--help` 안내와 잘못된 옵션 오류를 자동으로 제공한다.

직접 확인한다.

```zsh
python3 main.py --help
```

---

## 3. `pathlib.Path`: 상태 파일 위치 계산

관련 코드: [`src/state_manager.py`](../src/state_manager.py)

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE_PATH = PROJECT_ROOT / "state.json"
TEST_STATE_PATH = PROJECT_ROOT / "state.test.json"
```

### 왜 문자열 대신 `Path`를 사용하는가?

다음과 같이 경로를 문자열로 쓸 수도 있다.

```python
state_path = "state.json"
```

하지만 이 경로는 현재 터미널 위치를 기준으로 해석된다. 다른 폴더에서 프로그램을
실행하면 의도하지 않은 위치에서 파일을 찾을 수 있다.

`Path`는 경로를 하나의 객체로 표현하며 다음과 같은 기능을 제공한다.

```python
path.exists()       # 파일이 존재하는지 확인
path.open()         # 파일 열기
path.with_name(...) # 같은 폴더에서 이름이 다른 경로 만들기
path.replace(...)   # 다른 경로로 교체
```

### `__file__`

`__file__`은 현재 Python 소스 파일의 경로다. 이 코드는
`src/state_manager.py`에 있으므로 다음 위치를 나타낸다.

```text
프로젝트/src/state_manager.py
```

### `resolve()`

```python
Path(__file__).resolve()
```

상대 경로를 정리해 실제 절대 경로로 만든다. `.`과 `..` 같은 요소도 정리하고,
가능한 경우 심볼릭 링크도 실제 위치 기준으로 해석한다.

현재 터미널 위치가 아니라 현재 소스 파일의 실제 위치를 기준으로 경로를 계산하기
위해 사용한다.

### `parents[1]`

현재 파일이 `프로젝트/src/state_manager.py`라면 상위 폴더는 다음 순서다.

```text
parents[0] → 프로젝트/src
parents[1] → 프로젝트
```

따라서 `parents[1]`은 프로젝트 루트다.

### Path의 `/` 연산자

```python
PROJECT_ROOT / "state.json"
```

`Path` 객체에서 `/`는 경로를 연결한다.

```text
프로젝트 루트 / state.json
→ 프로젝트/state.json
```

### 학습 확인

다음 표현을 왼쪽부터 말로 풀어본다.

```python
Path(__file__).resolve().parents[1] / "state.json"
```

---

## 4. 기본 퀴즈와 리스트

관련 코드: [`src/default_quizzes.py`](../src/default_quizzes.py)

```python
def get_default_quizzes() -> list[Quiz]:
    return [
        Quiz(
            question="물의 화학식은 무엇인가요?",
            choices=["CO2", "H2O", "O2", "NaCl"],
            answer=2,
            hint="수소 원자 두 개와 산소 원자 한 개로 이루어져 있습니다.",
        ),
        ...
    ]
```

`get_default_quizzes()`는 `Quiz` 객체 다섯 개가 들어 있는 리스트를 반환한다.
정상 상태 파일을 읽을 때는 호출하지 않고 파일이 없거나 손상됐을 때만
`StateManager`가 호출한다.

```python
list[Quiz]
```

는 `Quiz` 객체를 담는 리스트라는 타입 힌트다.

### 왜 함수로 만드는가?

리스트는 변경 가능한 객체다.

```python
quizzes.append(new_quiz)
quizzes.pop()
```

기본 퀴즈를 하나의 전역 리스트로 계속 공유하면 다른 코드의 추가·삭제가 기본
데이터에도 영향을 줄 수 있다. 현재 함수는 호출할 때마다 새로운 리스트와 새로운
`Quiz` 객체를 만든다.

---

## 5. `Quiz` 클래스와 `dataclass`

관련 코드: [`src/quiz.py`](../src/quiz.py)

```python
from dataclasses import dataclass


@dataclass
class Quiz:
    question: str
    choices: list[str]
    answer: int
    hint: str
```

`Quiz` 클래스는 퀴즈 한 문제의 데이터와 동작을 묶는다.

### 클래스와 객체

- 클래스: 데이터 구조와 동작을 정의한 설계도
- 객체 또는 인스턴스: 클래스로 만든 실제 값
- 속성: 객체가 기억하는 데이터
- 메서드: 객체가 수행하는 기능

```python
quiz = Quiz(
    question="물의 화학식은?",
    choices=["CO2", "H2O", "O2", "NaCl"],
    answer=2,
    hint="수소와 산소를 생각해 보세요.",
)
```

위 코드로 만든 객체는 다음 속성을 가진다.

```python
quiz.question
quiz.choices
quiz.answer
quiz.hint
```

### `dataclass`가 필요한 이유

`dataclass`가 없다면 다음 생성자를 직접 작성해야 한다.

```python
class Quiz:
    def __init__(self, question, choices, answer, hint):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint
```

`@dataclass`는 위와 같은 `__init__()` 등을 자동으로 만들어 준다. 데이터 저장이
중심인 `Quiz`와 잘 맞는다. `dataclasses`도 Python 표준 라이브러리다.

### 타입 힌트

```python
question: str
choices: list[str]
answer: int
hint: str
```

타입 힌트는 각 속성에 어떤 종류의 값을 기대하는지 보여준다. 실행 중 모든 타입을
자동으로 강제하지는 않기 때문에 실제 검증은 `__post_init__()`에서 수행한다.

---

## 6. `__post_init__()`: 객체 생성 직후 검증

```python
def __post_init__(self) -> None:
    self.question = self._normalize_text(self.question, "문제")

    if not isinstance(self.choices, list) or len(self.choices) != 4:
        raise ValueError("선택지는 정확히 4개여야 합니다.")

    self.choices = [
        self._normalize_text(choice, f"선택지 {index}")
        for index, choice in enumerate(self.choices, start=1)
    ]

    if type(self.answer) is not int or not 1 <= self.answer <= 4:
        raise ValueError("정답 번호는 1부터 4 사이의 정수여야 합니다.")

    self.hint = self._normalize_text(self.hint, "힌트")
```

객체 생성 순서는 다음과 같다.

```text
Quiz(...) 호출
  → dataclass가 만든 __init__() 실행
  → 속성에 값 저장
  → __post_init__() 자동 실행
  → 문자열 정리와 형식 검증
```

검증 항목은 다음과 같다.

- 문제와 힌트는 비어 있지 않은 문자열이어야 한다.
- 선택지는 리스트이고 정확히 4개여야 한다.
- 각 선택지는 비어 있지 않은 문자열이어야 한다.
- 정답은 1부터 4 사이의 정수여야 한다.

### `self`

`self`는 현재 사용 중인 객체 자신을 가리킨다.

```python
self.answer
```

는 현재 `Quiz` 객체의 정답 번호다.

### `isinstance()`와 `len()`

```python
isinstance(self.choices, list)
len(self.choices) == 4
```

- `isinstance()`: 값이 지정한 타입인지 검사
- `len()`: 문자열이나 리스트 등의 길이 반환

### `raise ValueError`

잘못된 값으로 객체가 생성되는 것을 막기 위해 의도적으로 예외를 발생시킨다.
사용자 입력은 이미 한 번 검증하지만 JSON 파일이 직접 수정될 수도 있으므로 객체
경계에서 다시 검사한다.

### `@staticmethod`

```python
@staticmethod
def _normalize_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(...)
    return value.strip()
```

`_normalize_text()`는 다른 객체 속성을 사용하지 않고 전달받은 값만 검사한다. 그래서
`self`를 받지 않는 정적 메서드로 작성했다.

이름 앞의 `_`는 클래스 내부에서 사용하는 보조 기능이라는 관례다. Python이 외부
접근을 강제로 차단하는 것은 아니다.

### 리스트 컴프리헨션

```python
self.choices = [
    self._normalize_text(choice, f"선택지 {index}")
    for index, choice in enumerate(self.choices, start=1)
]
```

일반 반복문으로 풀면 다음과 같다.

```python
normalized_choices = []
for index, choice in enumerate(self.choices, start=1):
    normalized_choice = self._normalize_text(
        choice,
        f"선택지 {index}",
    )
    normalized_choices.append(normalized_choice)
self.choices = normalized_choices
```

선택지를 하나씩 정리해 새로운 리스트로 만든다. 새 리스트를 만드는 이유는 호출자가
전달한 원본 리스트와 `Quiz` 내부 리스트의 변경을 분리하기 위해서다.

---

## 7. 객체 조립과 `__init__()`

`main()`은 `StateManager`와 `GameManager`를 다음과 같이 만든다.

```python
state_manager = StateManager(state_path)
game_manager = GameManager(state_manager)
```

### `StateManager.__init__()`

```python
def __init__(self, state_path: Path) -> None:
    self.state_path = state_path
    self._save_enabled = True
```

`__init__()`은 객체를 만들 때 자동 실행되는 초기화 메서드다.

- `state_path`: 읽고 쓸 JSON 파일 위치
- `_save_enabled`: 현재 실행에서 저장할 수 있는지 나타내는 `bool`

기본 퀴즈를 속성으로 계속 보관하지 않고 실제로 필요한 복구 시점에 새로 만든다.

### 단순해진 `GameManager.__init__()`

```python
def __init__(self, state_manager: StateManager) -> None:
    self.quizzes: list[Quiz] = []
    self.best_score: int | None = None
    self.score_history: list[ScoreRecord] = []
    self.state_manager = state_manager
    self.timed_input = TimedTerminalInput()
```

`GameManager`는 빈 상태로 생성된 후 JSON에서 실제 상태를 불러온다.

```text
기본 데이터와 파일 관리 → StateManager
현재 게임 진행과 상태 사용 → GameManager
```

`GameManager`가 JSON을 직접 처리하지 않고 전달받은 `StateManager`에 요청하는 구조다.
상속을 사용하지 않고 한 객체가 다른 객체를 포함해 사용하는 객체 합성이다.

---

## 8. `ScoreRecord`: 타입에 이름 붙이기

```python
ScoreRecord = dict[str, str | int]
```

이 코드는 새로운 클래스나 객체를 만드는 것이 아니라 긴 타입에 이름을 붙이는 타입
별칭이다.

실제 기록은 다음 형태다.

```python
{
    "played_at": "2026-08-09 15:30",
    "score": 7,
}
```

키는 문자열이고 값은 문자열 또는 정수다. 이를 매번
`dict[str, str | int]`로 쓰지 않고 `ScoreRecord`라는 이름으로 표현한다.

```python
self.score_history: list[ScoreRecord] = []
```

는 점수 기록 딕셔너리들을 보관하는 리스트라는 뜻이다.

---

## 9. JSON 상태 불러오기

`main()`은 객체를 만든 뒤 다음 순서로 실행한다.

```python
game_manager.load_state()
game_manager.run()
```

먼저 저장된 상태를 복원하고, 복원이 끝난 뒤 메뉴를 시작한다.

### `GameManager.load_state()`

```python
(
    self.quizzes,
    self.best_score,
    self.score_history,
) = self.state_manager.load_state()
```

`StateManager.load_state()`가 반환한 세 값을 각각의 속성으로 나눠 받는다. 이를 튜플
반환과 구조 분해 할당이라고 한다.

### 파일이 없는 첫 실행

```python
if not self.state_path.exists():
    default_state = self._create_default_state()
    self.save_state(*default_state)
    return default_state
```

`Path.exists()`는 해당 경로에 파일이 있으면 `True`, 없으면 `False`를 반환한다.

기본 상태는 다음 세 값이다.

```python
return get_default_quizzes(), None, []
```

- 기본 퀴즈 목록
- 아직 최고 점수가 없다는 `None`
- 빈 플레이 기록 리스트

`None`은 0과 다르다. `None`은 아직 플레이한 적이 없다는 의미이고, 0점은 플레이한
결과가 0점이라는 의미다.

### `*`로 인자 펼치기

```python
self.save_state(*default_state)
```

다음 코드와 같은 의미다.

```python
self.save_state(
    default_state[0],
    default_state[1],
    default_state[2],
)
```

### 파일 읽기와 `with`

```python
with self.state_path.open("r", encoding="utf-8") as file:
    state_data = json.load(file)
```

- `"r"`: 읽기 모드
- `encoding="utf-8"`: 한글을 올바르게 읽는 문자 인코딩
- `with`: 블록이 끝나면 파일을 자동으로 닫음
- `json.load(file)`: JSON 파일을 Python 딕셔너리와 리스트로 변환

파일을 직접 열고 `close()`를 호출하는 방식보다 `with`를 사용하면 중간에 예외가
발생해도 파일이 정리된다.

---

## 10. JSON 검증과 `Quiz` 객체 복원

```python
if not isinstance(state, dict):
    raise ValueError("상태 데이터는 객체 형식이어야 합니다.")
```

JSON의 최상위 객체는 Python에서 `dict`로 읽힌다.

```python
quizzes_data = state.get("quizzes")
score_history_data = state.get("score_history")
```

`dict.get()`은 키의 값을 가져오고 키가 없으면 `None`을 반환한다.

```python
if not isinstance(quizzes_data, list):
    raise ValueError("quizzes는 목록이어야 합니다.")
```

### 객체를 바로 JSON에 저장할 수 없는 이유

JSON은 Python의 `Quiz` 클래스를 알지 못한다. JSON은 문자열, 숫자, `null`, 배열,
객체 같은 공통 데이터 형식만 표현한다.

따라서 저장할 때는 객체를 딕셔너리로 바꾼다.

```python
quiz.to_dict()
```

불러올 때는 딕셔너리에서 다시 객체를 만든다.

```python
Quiz.from_dict(data)
```

전체 경계는 다음과 같다.

```text
저장:
Quiz 객체 → to_dict() → dict → json.dump() → state.json

불러오기:
state.json → json.load() → dict → Quiz.from_dict() → Quiz 객체
```

### `@classmethod`

```python
@classmethod
def from_dict(cls, data: object) -> "Quiz":
    ...
    return cls(
        question=data["question"],
        choices=data["choices"],
        answer=data["answer"],
        hint=data["hint"],
    )
```

`classmethod`는 기존 객체인 `self` 대신 현재 클래스인 `cls`를 받는다. 딕셔너리에서
새 `Quiz` 객체를 만드는 대체 생성 방식으로 사용한다.

`cls(...)`로 객체를 만들면 `__post_init__()`도 다시 실행되므로 JSON에서 불러온
데이터도 같은 검증을 받는다.

### 필수 필드 확인

```python
required_fields = ("question", "choices", "answer", "hint")
missing_fields = [
    field for field in required_fields if field not in data
]
```

현재 버전에서는 문제, 선택지, 정답과 힌트가 모두 필수다.

---

## 11. 점수와 기록 데이터 검증

```python
loaded_score = state.get("best_score")
if "best_score" not in state or (
    loaded_score is not None
    and (type(loaded_score) is not int or loaded_score < 0)
):
    raise ValueError(...)
```

최고 점수는 다음 둘 중 하나여야 한다.

- 아직 플레이하지 않았으면 `None`
- 플레이했다면 0 이상의 `int`

### 왜 `type(value) is int`인가?

Python의 `bool`은 정수 타입과 관련이 있어 다음 결과가 참이다.

```python
isinstance(True, int)  # True
```

하지만 `True`를 점수로 인정하면 안 된다. 정확한 정수인지 확인하기 위해
`type(value) is int`를 사용한다.

현재 플레이 기록은 다음 두 필드만 검증한다.

```python
{
    "played_at": 문자열,
    "score": 0 이상의 정수,
}
```

---

## 12. `try-except`: 파일 오류와 손상 복구

```python
try:
    with self.state_path.open("r", encoding="utf-8") as file:
        state_data = json.load(file)
    loaded_state = self.validate_state_data(state_data)
except OSError as error:
    ...
except (json.JSONDecodeError, UnicodeError, TypeError, ValueError) as error:
    ...
```

`try`에는 오류가 발생할 수 있는 코드를 넣고, `except`는 특정 오류가 발생했을 때
실행할 코드를 정의한다.

| 예외 | 대표 상황 |
|---|---|
| `OSError` | 파일 권한, 디스크, 읽기·쓰기 오류 |
| `JSONDecodeError` | JSON 괄호나 쉼표 등 문법 오류 |
| `UnicodeError` | 문자 인코딩 오류 |
| `TypeError`, `ValueError` | 데이터 타입·범위·필드 오류 |

### 손상 파일 복구 흐름

```text
JSON 손상 안내
  → 기본 상태 준비
  → shutil.copy2()로 손상 원본 백업
  → 기본 상태를 새 상태 파일에 저장
  → 기본 퀴즈로 게임 실행
```

```python
shutil.copy2(self.state_path, backup_path)
```

`shutil`은 파일 복사와 이동을 제공하는 표준 라이브러리다. `copy2()`는 파일 내용과
가능한 메타데이터를 함께 복사한다.

백업 파일 이름에는 현재 시각을 넣는다.

```python
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
```

- `datetime.now()`: 현재 로컬 날짜와 시각
- `strftime()`: 날짜와 시각을 지정한 형식의 문자열로 변환

백업 파일명은 초 단위까지만 사용한다. 같은 초에 같은 이름의 백업이 이미 있으면
`-1`, `-2`처럼 순번을 붙여 기존 백업을 덮어쓰지 않는다.

백업에 실패하면 손상 원본을 덮어쓰지 않도록 저장을 비활성화한다.

```python
self._save_enabled = False
```

---

## 13. 메뉴 반복과 공통 입력 검증

관련 코드: [`src/game_manager.py`](../src/game_manager.py)

```python
def run(self) -> None:
    menu_actions = {
        1: self.play_quizzes,
        2: self.list_quizzes,
        3: self.show_score_records,
        4: self.add_quiz,
        5: self.delete_quiz,
        6: self.safe_exit,
    }
    try:
        while True:
            self.show_menu()
            choice = self.read_int("메뉴 선택(1~6): ", 1, 6)
            menu_actions[choice]()
            if choice == 6:
                return
    except (KeyboardInterrupt, EOFError):
        self.safe_exit(interrupted=True)
```

### 메뉴 딕셔너리

```python
MENU_ITEMS = {
    1: "퀴즈 풀기",
    2: "퀴즈 목록 보기",
    3: "최고 점수와 기록",
    4: "퀴즈 추가",
    5: "퀴즈 삭제",
    6: "종료",
}
```

`dict`는 키와 값을 연결한다. `dict.items()`는 키와 값을 한 쌍씩 반환한다.

```python
for number, label in self.MENU_ITEMS.items():
    print(f"{number}. {label}")
```

`f"..."`는 문자열 안에 변수 값을 넣는 f-string이다.

### `while True`

사용자가 종료를 선택할 때까지 메뉴를 계속 반복한다. 기능 하나가 끝나면 반복문의
처음으로 돌아가 메뉴를 다시 보여준다.

### 숫자 입력 흐름

```python
raw_value = input(prompt).strip()
```

`input()`의 결과는 사용자가 숫자를 입력해도 항상 문자열이다.

```text
input()      → " 3 "
strip()      → "3"
int("3")     → 3
범위 검사    → 정상
return 3
```

빈 입력은 다음과 같이 처리한다.

```python
if not raw_value:
    print("입력값이 비어 있습니다.")
    continue
```

숫자로 변환할 수 없는 입력은 예외 처리한다.

```python
try:
    value = int(raw_value)
except ValueError:
    print("숫자만 입력해 주세요.")
    continue
```

`continue`는 현재 반복의 나머지 코드를 건너뛰고 `while`의 처음으로 돌아간다.

정상 범위의 숫자이면 값을 반환하고 함수가 끝난다.

```python
if minimum <= value <= maximum:
    return value
```

입력 검증을 공통 메서드로 만든 이유는 메뉴, 정답 번호, 문제 수와 삭제 번호에서 같은
코드를 반복하지 않기 위해서다.

---

## 14. 메뉴 기능 선택

```python
menu_actions = {
    1: self.play_quizzes,
    2: self.list_quizzes,
    3: self.show_score_records,
    4: self.add_quiz,
    5: self.delete_quiz,
    6: self.safe_exit,
}

menu_actions[choice]()
```

Python에서는 함수와 메서드도 변수에 담을 수 있는 객체다. 딕셔너리 값에 실제로
호출할 메서드를 저장하고, 입력 번호를 키로 사용해 선택한 메서드를 가져온다.

```python
menu_actions[1]    # self.play_quizzes 메서드 객체
menu_actions[1]()  # 메서드 호출
```

C의 함수 포인터와 목적이 비슷하지만 Python에서는 별도의 포인터 문법 없이 함수와
메서드 자체를 값으로 저장한다. 메뉴 기능을 추가할 때 긴 `if/elif` 분기를 늘리지
않고 딕셔너리에 번호와 메서드를 추가할 수 있다.

조회·추가·삭제·플레이 메서드가 끝나면 `while True`의 처음으로 돌아간다. 종료
메서드도 딕셔너리를 통해 실행한다. 다만 `safe_exit()`은 안내와 저장만 담당하므로,
6번 실행 후에는 `return`으로 `run()` 반복도 끝낸다.

---

## 15. 퀴즈 추가와 롤백

```text
문제 입력
  → 선택지 4개 입력
  → 정답 번호 입력
  → 힌트 입력
  → Quiz 객체 생성과 검증
  → 메모리 리스트에 추가
  → JSON 저장
```

선택지 입력에는 `range()`와 리스트 컴프리헨션을 사용한다.

```python
choices = [
    self.read_nonempty(f"선택지 {number}: ")
    for number in range(1, 5)
]
```

`range(1, 5)`는 `1, 2, 3, 4`를 만든다. 따라서 선택지를 네 번 입력받는다.

입력값으로 `Quiz` 객체를 만든 뒤 리스트에 추가한다.

```python
new_quiz = Quiz(...)
self.quizzes.append(new_quiz)
```

메모리 추가와 파일 저장이 모두 성공해야 실제 기능 성공으로 판단한다.

```python
if self.save_state():
    return True

self.quizzes.pop()
return False
```

저장에 실패하면 `pop()`으로 방금 추가한 객체를 제거한다. 파일과 메모리 상태의
불일치를 막기 위해 변경을 이전 상태로 되돌리는 롤백이다.

---

## 16. 퀴즈 목록과 삭제

### `enumerate()`로 목록 출력

```python
for number, quiz in enumerate(self.quizzes, start=1):
    print(f"{number}. {quiz.question}")
```

`enumerate()`는 리스트 값과 순번을 함께 제공한다. 사용자가 보는 번호는 1부터
시작하므로 `start=1`을 사용한다.

### 사용자 번호와 리스트 인덱스

Python 리스트는 0번부터 시작하지만 사용자에게 보여준 번호는 1번부터 시작한다.

```python
quiz_index = choice - 1
```

```text
사용자 번호 1 → 리스트 인덱스 0
사용자 번호 2 → 리스트 인덱스 1
```

삭제할 객체를 먼저 기억하고 리스트에서 제거한다.

```python
selected_quiz = self.quizzes[quiz_index]
self.quizzes.pop(quiz_index)
```

저장 실패 시 원래 위치에 복원한다.

```python
self.quizzes.insert(quiz_index, selected_quiz)
```

현재 버전에서는 퀴즈를 모두 삭제해도 이전 플레이의 최고 점수는 유지된다.

---

## 17. 퀴즈 플레이와 `random.sample()`

```text
등록된 문제 수 확인
  → 풀 문제 수 입력
  → 중복 없는 무작위 문제 선택
  → 문제별 제한시간 답 입력
  → 정답 판정과 점수 계산
  → 플레이 기록 저장
```

현재 코드는 별도 문제 수 선택 메서드 없이 `play_quizzes()` 안에서 바로 입력받는다.

```python
total_quizzes = len(self.quizzes)
quiz_count = self.read_int(
    f"풀 문제 수를 입력하세요(1~{total_quizzes}): ",
    1,
    total_quizzes,
)
```

문제 선택에는 `random` 표준 라이브러리를 사용한다.

```python
selected_quizzes = random.sample(self.quizzes, k=quiz_count)
```

`random.sample()`은 원본 리스트에서 `k`개를 중복 없이 골라 새로운 리스트로
반환한다.

- `random.shuffle()`: 원본 리스트 순서를 직접 변경
- `random.sample()`: 원본은 유지하고 새 무작위 리스트 반환

상태 파일의 문제 순서는 유지하고 이번 출제 순서만 바꾸기 위해 `sample()`을
사용한다.

### 객체에게 동작 요청

```python
quiz.display(number=number)
```

현재 `Quiz` 객체가 자신의 문제와 선택지를 출력한다.

```python
quiz.is_correct(answer_result.answer)
```

현재 `Quiz` 객체가 사용자의 답과 자신의 정답을 비교한다. 문제 데이터와 정답 판정
규칙을 `Quiz` 한곳에 둔다.

---

## 18. 제한시간 입력

관련 코드: [`src/timed_input.py`](../src/timed_input.py)

```python
answer_result = self.timed_input.read_answer(quiz.hint)
```

일반 `input()`은 Enter를 누를 때까지 프로그램 실행을 멈춘다. 이 상태에서는 다음
기능을 동시에 처리하기 어렵다.

- 1초마다 남은 시간 갱신
- 5초 뒤 자동 힌트 공개
- 10초 뒤 자동 시간 초과

그래서 제한시간 입력은 별도 `TimedTerminalInput` 클래스가 담당한다.

### 결과 객체

```python
@dataclass(frozen=True)
class TimedAnswerResult:
    answer: int | None
    hint_shown: bool
```

- `answer`: 사용자가 입력한 1~4, 시간 초과이면 `None`
- `hint_shown`: 힌트가 공개됐는지 나타내는 `bool`
- `frozen=True`: 생성 후 결과 속성을 변경할 수 없음

`GameManager`는 제한시간 내부 구현 전체를 알 필요 없이 다음 두 값만 사용한다.

```python
answer_result.answer
answer_result.hint_shown
```

### `time.monotonic()`

```python
started_at = time.monotonic()
hint_at = started_at + 5
deadline = started_at + 10
```

`datetime.now()`는 현재 날짜와 시각을 기록할 때 사용한다. `time.monotonic()`은
얼마나 시간이 지났는지 측정할 때 사용한다. 시스템 시계가 변경돼도 뒤로 가지 않아
제한시간 계산에 적합하다.

### `select.select()`

```python
readable, _, _ = select.select(
    [sys.stdin],
    [],
    [],
    wait_seconds,
)
```

입력을 무한정 기다리지 않고 지정한 시간만 기다린다. 입력이 없으면 다시 코드로
돌아와 현재 시간, 힌트 공개 시점과 남은 시간을 검사한다.

```text
현재 시간 확인
  → 힌트 시각 확인
  → 남은 시간 계산
  → 잠시 입력 대기
  → 다시 현재 시간 확인
```

### `termios`와 터미널 복원

`termios`는 macOS 같은 POSIX 터미널의 입력 모드를 제어한다. 사용자가 입력하는
문자를 코드가 직접 관리할 수 있도록 입력 모드를 잠시 변경한다.

```python
finally:
    termios.tcsetattr(
        sys.stdin.fileno(),
        termios.TCSANOW,
        original_settings,
    )
```

`finally`는 정상 반환과 예외 발생 여부에 관계없이 실행된다. 따라서 시간 초과나
Ctrl+C에서도 원래 터미널 설정을 복구한다.

ANSI 제어 문자는 현재 줄을 지우거나 커서를 이동해 카운트다운을 같은 위치에 다시
그리는 데 사용한다.

이 파일은 미션의 기본 Python 문법보다 심화된 부분이다. 우선 `read_answer()`가 답과
힌트 공개 여부를 반환한다는 객체 경계를 이해한 뒤 내부 입출력 처리를 학습한다.

---

## 19. 정답 판정과 점수 계산

점수는 0에서 시작하고 각 문제 결과를 처리할 때 바로 변경한다.

```python
score = 0
```

시간 초과, 정답과 오답을 하나의 `if/elif/else` 흐름으로 처리한다.

```python
if answer_result.answer is None:
    print("시간 초과입니다.")
elif quiz.is_correct(answer_result.answer):
    correct_count += 1
    score += self.CORRECT_POINTS
    if answer_result.hint_shown:
        score -= self.HINT_PENALTY
    print("정답입니다!")
else:
    print("오답입니다.")

print(f"현재 점수: {score}점")
```

점수는 클래스 상수로 정의되어 있다.

```python
CORRECT_POINTS = 3
HINT_PENALTY = 2
```

숫자의 의미를 이름으로 보여주고 점수 규칙을 한곳에서 수정하기 위해서다. 정답이면
현재 점수에 3점을 더하고, 그 정답에서 힌트를 봤다면 바로 2점을 차감한다.

차감 코드는 정답 분기 안에만 있다. 따라서 힌트를 봤더라도 오답이거나 시간 초과이면
점수가 바뀌지 않는다. 문제별 처리가 끝날 때 공통으로 현재 누적 점수를 출력하므로
사용자는 진행 중에도 게임 상태를 확인할 수 있다.

오답이면 사용자 정답 번호를 리스트 인덱스로 바꿔 정답 선택지를 찾는다.

```python
correct_choice = quiz.choices[quiz.answer - 1]
```

---

## 20. 최고 점수와 플레이 기록

현재 기록은 플레이 시각과 점수만 저장한다.

```python
record: ScoreRecord = {
    "played_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "score": score,
}
```

`datetime.now()`으로 현재 시각을 얻고 `strftime()`으로 JSON에 저장하기 쉬운 문자열로
바꾼다.

최고 점수는 별도 메서드 없이 직접 비교한다.

```python
is_new_best = self.best_score is None or score > self.best_score
if is_new_best:
    self.best_score = score
```

기록 추가와 최고 점수 변경 후 한 번 저장한다.

```python
self.score_history.append(record)
```

저장에 실패하면 두 변경을 모두 되돌린다.

```python
self.score_history.pop()
self.best_score = previous_score
```

### 최근 기록 5개

```python
recent_history = self.score_history[-5:]
recent_history.reverse()
```

`[-5:]` 슬라이싱은 마지막 5개를 새 리스트로 가져온다. `reverse()`는 그 새 리스트를
뒤집어 최신 기록부터 출력하게 한다. 원본 `score_history`의 순서는 바뀌지 않는다.

---

## 21. JSON 저장과 임시 파일

```python
state_data = {
    "quizzes": [quiz.to_dict() for quiz in quizzes],
    "best_score": best_score,
    "score_history": score_history,
}
```

`Quiz` 객체를 딕셔너리로 변환해 JSON이 저장할 수 있는 상태를 만든다.

### 임시 파일을 먼저 쓰는 이유

```python
temp_path = self.state_path.with_name(f"{self.state_path.name}.tmp")
```

`state.json`을 사용하는 경우 임시 경로는 `state.json.tmp`가 된다.

```python
with temp_path.open("w", encoding="utf-8", newline="\n") as file:
    json.dump(state_data, file, ensure_ascii=False, indent=4)
    file.write("\n")
temp_path.replace(self.state_path)
```

- `"w"`: 쓰기 모드
- `encoding="utf-8"`: 한글 저장
- `ensure_ascii=False`: 한글을 `\u...` 형태로 바꾸지 않음
- `indent=4`: 사람이 읽기 쉽도록 들여쓰기 4칸
- `replace()`: 완성된 임시 파일을 실제 상태 파일로 교체

실제 파일에 바로 쓰다가 중단되면 기존 파일까지 손상될 수 있다. 임시 파일을 완성한
뒤 교체하면 이 위험을 줄일 수 있다.

저장 실패 시 남은 임시 파일을 정리한다.

```python
try:
    temp_path.unlink(missing_ok=True)
except OSError:
    pass
```

`unlink()`는 파일을 삭제한다. `missing_ok=True`이면 이미 파일이 없어도 예외를
발생시키지 않는다. 정리 작업 자체가 실패해도 원래 저장 오류 처리를 계속하기 위해
두 번째 `OSError`는 `pass`로 넘긴다.

---

## 22. 안전 종료

메뉴 전체는 입력 중단 예외를 처리한다.

```python
try:
    while True:
        ...
except (KeyboardInterrupt, EOFError):
    self.safe_exit(interrupted=True)
```

- `KeyboardInterrupt`: 사용자가 Ctrl+C 입력
- `EOFError`: 입력 스트림 종료

메뉴 입력 하나가 아니라 전체 메뉴 반복을 감싸므로 추가, 삭제와 플레이 중 발생한
입력 중단도 같은 방식으로 처리한다.

```python
def safe_exit(self, interrupted: bool = False) -> None:
    self.save_state()
    if interrupted:
        print("입력이 중단되었습니다.")
    print("게임을 종료합니다.")
```

가능한 현재 상태를 한 번 더 저장하고 traceback 없이 종료한다.

---

## 23. 클래스별 책임 정리

| 클래스 | 보관하는 데이터 | 주요 동작 |
|---|---|---|
| `Quiz` | 문제, 선택지, 정답, 힌트 | 검증, 출력, 정답 판정, 딕셔너리 변환 |
| `GameManager` | 현재 퀴즈, 최고 점수, 기록 | 메뉴, 입력, 플레이, 추가·삭제, 점수 처리 |
| `StateManager` | 파일 경로, 저장 가능 상태 | JSON 저장·검증·백업·복구 |
| `TimedTerminalInput` | 제한시간과 힌트 시각 설정 | 카운트다운, 답 입력, 자동 힌트, 시간 초과 |

이 분리는 한 클래스가 모든 기능을 처리하지 않게 한다.

```text
GameManager ──저장 요청──> StateManager ──읽기/쓰기──> JSON 파일
    │
    ├──여러 Quiz 객체 관리
    └──답 입력 요청──> TimedTerminalInput
```

---

## 24. 강의장에서 따라갈 코드 순서

다음 순서로 파일을 열면 난이도가 자연스럽게 올라간다.

1. [`main.py`](../main.py)
   - import, 함수, `argparse`, 객체 생성, 프로그램 진입점
2. [`src/default_quizzes.py`](../src/default_quizzes.py)
   - 함수 반환값, 리스트, `Quiz` 객체 생성
3. [`src/quiz.py`](../src/quiz.py)
   - 클래스, `dataclass`, `self`, 검증, 객체와 딕셔너리 변환
4. [`src/game_manager.py`](../src/game_manager.py)
   - 입력, 조건문, 반복문, 리스트 변경, 게임 흐름과 롤백
5. [`src/state_manager.py`](../src/state_manager.py)
   - `Path`, JSON, 파일 입출력, 예외 처리와 복구
6. [`src/timed_input.py`](../src/timed_input.py)
   - 제한시간 입력과 터미널 제어 심화 기능

`timed_input.py`는 마지막에 본다. 먼저 `read_answer()`가 `TimedAnswerResult`를
반환한다는 공개 동작을 이해한 뒤 내부의 `select`, `termios`와 ANSI 제어를 읽는다.

---

## 25. 동료평가 설명 순서

1. `main.py`가 프로그램의 진입점이라고 설명한다.
2. `argparse`가 `--test` 옵션을 `bool`로 바꾸는 과정을 설명한다.
3. `Path(__file__).resolve().parents[1]`로 프로젝트 루트를 찾는 이유를 설명한다.
4. 기본 퀴즈 함수가 새 `Quiz` 객체 목록을 반환한다고 설명한다.
5. `Quiz`가 `dataclass`이고 `__post_init__()`에서 형식을 검증한다고 설명한다.
6. `StateManager`와 `GameManager`를 만들고 상태를 불러오는 순서를 설명한다.
7. JSON 딕셔너리를 `Quiz.from_dict()`로 객체로 복원하는 과정을 설명한다.
8. 파일 없음과 손상 JSON을 `try-except`로 처리하는 방식을 설명한다.
9. `while True` 메뉴와 `read_int()` 공통 입력 검증을 설명한다.
10. 추가·삭제·플레이 후 저장하고 실패하면 롤백한다고 설명한다.
11. `random.sample()`을 선택한 이유를 설명한다.
12. 제한시간 입력에서 `select.select()`와 `time.monotonic()`의 역할을 설명한다.
13. 시각과 점수만 저장하는 단순한 플레이 기록 구조를 설명한다.
14. 임시 JSON 파일을 쓴 뒤 실제 파일로 교체하는 이유를 설명한다.
15. Ctrl+C와 EOF에서 가능한 상태를 저장하고 안전 종료한다고 설명한다.

---

## 26. 최종 학습 체크리스트

다음 질문에 코드를 가리키며 답할 수 있는지 확인한다.

- [ ] `import`한 표준 라이브러리와 프로젝트 모듈을 구분할 수 있다.
- [ ] `argparse`의 `store_true`가 무엇을 반환하는지 설명할 수 있다.
- [ ] `Path(__file__).resolve().parents[1]`을 왼쪽부터 설명할 수 있다.
- [ ] 함수의 매개변수, 반환값과 타입 힌트를 구분할 수 있다.
- [ ] 클래스, 객체, 속성, 메서드와 `self`를 설명할 수 있다.
- [ ] `dataclass`가 자동으로 만들어 주는 생성자의 역할을 설명할 수 있다.
- [ ] `__post_init__()`, `staticmethod`, `classmethod`의 사용 이유를 설명할 수 있다.
- [ ] `list`, `dict`, `tuple`, `None`이 코드에서 어디에 쓰이는지 찾을 수 있다.
- [ ] `if`, `for`, `while`, `continue`, `return`의 실행 흐름을 설명할 수 있다.
- [ ] 리스트 컴프리헨션을 일반 `for` 문으로 풀어 쓸 수 있다.
- [ ] JSON과 `Quiz` 객체 사이에 변환이 필요한 이유를 설명할 수 있다.
- [ ] `with`, `json.load()`, `json.dump()`의 역할을 설명할 수 있다.
- [ ] `try-except`가 입력 오류와 파일 오류에서 어떻게 사용되는지 설명할 수 있다.
- [ ] 저장 실패 시 추가·삭제·점수 변경을 되돌리는 이유를 설명할 수 있다.
- [ ] `random.sample()`과 `random.shuffle()`의 차이를 설명할 수 있다.
- [ ] `datetime.now()`와 `time.monotonic()`의 목적 차이를 설명할 수 있다.
- [ ] 일반 `input()`만으로 제한시간 구현이 어려운 이유를 설명할 수 있다.
- [ ] 임시 파일 작성 후 `replace()`하는 이유를 설명할 수 있다.
- [ ] Ctrl+C와 EOF가 어디에서 처리되는지 찾을 수 있다.

## 한 문장 정리

이 프로그램은 `main.py`에서 실행 옵션과 객체를 준비하고, `StateManager`가 JSON을
`Quiz` 객체로 복원한 뒤, `GameManager`가 메뉴와 게임을 진행하며, 상태가 바뀔 때마다
다시 JSON으로 안전하게 저장하는 구조다.
