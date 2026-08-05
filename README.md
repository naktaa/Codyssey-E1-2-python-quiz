# E1-2 나만의 퀴즈 게임

> 현재 상태: `main`에 JSON 저장·불러오기와 손상 복구를 병합했고, 기본 상식
> 퀴즈 5개와 최고 점수 재실행 유지까지 반영했다.

## 프로젝트 개요

터미널 메뉴에서 카테고리별 퀴즈를 풀고, 새 문제를 추가하고, 문제 목록과
최고 점수를 확인하는 Python 콘솔 프로그램이다. 퀴즈와 카테고리별 최고 점수는
프로젝트 루트의 JSON 파일에 저장한다.

## 퀴즈 주제와 선정 이유

- 주제: 여러 카테고리로 구성된 상식 퀴즈
- 선정 이유: 다양한 분야의 지식을 카테고리별로 나누어 학습하고 확인하기 위함
- 현재 데이터: 과학 3개·역사 2개, 총 5개의 기본 상식 문제

## 개발 환경과 실행 방법

- macOS / zsh
- Python 3.12.13 (요구 버전 3.10 이상)
- Git 2.53.0
- 외부 라이브러리 없음

실제 게임 데이터인 `state.json`을 사용한다.

```zsh
python --version
python main.py
```

사용자 환경에서는 `py` 명령으로도 `main.py`가 실행되도록 설정되어 있다.

직접 기능을 확인하면서 실제 게임 데이터를 바꾸고 싶지 않을 때는 다음처럼
환경 변수로 확인용 상태 파일을 선택한다.

```zsh
QUIZ_STATE_MODE=test py
```

이 모드는 `[테스트 모드] state.test.json을 사용합니다.`를 먼저 출력하고
프로젝트 루트의 `state.test.json`만 읽고 쓴다. 이 파일과 복구 과정에서 생기는
`*.corrupt-*` 파일은 `.gitignore`에 포함되어 기능 확인 중의 데이터 변경이
커밋에 들어가지 않는다. 환경 변수를 지정하지 않거나 `real`로 지정하면
`state.json`을 사용한다.

### 검증 원칙

2026-08-05 이후에는 `unittest`를 실행하거나 수정하지 않는다. `tests/`는 이전
개발 과정의 기록으로만 남겨 두며 현재 기능의 정상 근거로 사용하지 않는다.
앞으로의 기능 검증은 사용자가 `main.py`를 직접 실행한 원본 로그나 캡처로
확인한다. 과거 작업 기록에 적힌 unittest 결과는 당시 수행 사실을 보존한
것이며 현재 JSON 구현의 검증 결과를 뜻하지 않는다.

## 기능과 현재 상태

| 기능 | 구현 내용 | 현재 상태 |
|---|---|---|
| 메뉴·공통 입력 | 메뉴 1~5, 빈 값·문자·범위 밖 숫자 재입력 | 직접 실행 확인 |
| 퀴즈 풀기 | 카테고리 선택, 순차 출제, 정오답·환산 점수 출력 | 직접 실행 확인 |
| 풀이 문제 수 | 카테고리의 전체 문제 중 풀 개수를 1~전체 범위에서 선택 | 구현 완료, 직접 확인 필요 |
| 무작위 출제 | 선택한 문제 수만큼 중복 없이 뽑아 무작위 순서로 출제 | 구현 완료, 직접 확인 필요 |
| 퀴즈 추가 | 카테고리·문제·선택지 4개·정답 입력 후 즉시 저장 | 구현 완료, JSON 저장 화면 증거 필요 |
| 퀴즈 목록 | 카테고리별 문제와 가로형 선택지, 문제 사이 빈 줄 | 캡처 확보 |
| 최고 점수 | 카테고리별 0~100점 비교·갱신·즉시 저장 | 종료·재실행 유지 로그 확보 |
| JSON 불러오기 | 정상 데이터를 `Quiz`와 최고 점수로 복원 | 최고 점수 복원 확인, 추가 퀴즈 확인 필요 |
| JSON 저장 | UTF-8 임시 파일 작성 후 교체 | 구현 완료 |
| 실행 모드 분리 | 실제 `state.json`과 확인용 `state.test.json` 분리 | 구현 완료 |
| 손상 복구 | 오류 안내, 원본 백업, 기본 데이터 복구 | 직접 실행 캡처·백업 내용 확보 |
| 안전 종료 | 정상 종료·Ctrl+C·EOF에서 저장 후 안내 | 직접 실행 로그·캡처 확보 |

## 주요 코드 구조와 메서드

- `main.py`: 실행 모드에 맞는 상태 경로를 정하고 `QuizGame.load_state()` 후
  `QuizGame.run()`을 호출한다.
- `src/quiz.py`의 `Quiz`: 문제 데이터 검증, `display()`, `is_correct()`,
  `to_dict()`, `from_dict()`를 담당한다.
- `src/game_manager.py`의 `QuizGame`: 입력과 메뉴, 플레이, 추가, 목록, 점수,
  저장·불러오기와 복구 흐름을 관리한다.
- `select_quiz_count()`: 선택한 카테고리의 전체 문제 수를 안내하고 풀 문제 수를
  공통 숫자 입력 검증으로 받는다.
- `random.sample()`: 원본 퀴즈와 JSON 순서는 유지하면서 이번 플레이에 사용할
  문제를 중복 없이 선택하고 반환된 무작위 순서대로 출제한다.
- `save_state()`: 퀴즈와 점수를 임시 JSON 파일에 쓴 뒤 실제 상태 파일로
  교체해 부분 저장 가능성을 줄인다.
- `validate_state_data()`: JSON 최상위 구조, 퀴즈 목록과 점수 값을 검증한다.
- `backup_corrupted_state()`: 손상 원본을 timestamp가 붙은 이름으로 복사한다.
- `recover_corrupted_state()`: 백업 성공 후에만 기본 데이터로 활성 상태 파일을
  다시 만든다. 백업이 실패하면 원본 보호를 위해 해당 실행의 저장을 막는다.
- `safe_exit()`: 정상 종료와 입력 중단 시 가능한 현재 상태를 저장하고 종료한다.

## 데이터 영속성

### 실제 게임 데이터

- 파일: 프로젝트 루트의 `state.json`
- 용도: 실제 퀴즈 목록과 카테고리별 최고 점수
- Git: 미션 산출물이므로 추적
- 저장 시점: 퀴즈 추가 직후, 최고 점수 갱신 직후, 정상·중단 종료 시

### 직접 확인용 데이터

- 파일: 프로젝트 루트의 `state.test.json`
- 선택 방법: `QUIZ_STATE_MODE=test`
- 용도: 실제 게임 데이터를 바꾸지 않는 사용자 직접 실행 확인
- Git: 변경이 반복되므로 추적하지 않음

### 영속성 검증 상태

- JSON 적용 전: 추가한 문제가 재실행 후 사라지는 메모리 동작을
  [비교 기준 로그](evidence/logs/memory-persistence-test.md)로 보존했다.
- JSON 적용 후 코드: 퀴즈 추가와 최고 점수 갱신 시 파일 저장, 시작 시 파일
  불러오기가 연결되어 있다.
- JSON 적용 후 최고 점수: 과학 100점을 저장하고 종료한 뒤 같은 확인용 파일로
  재실행해 100점이 복원되는 것을
  [원본 로그](evidence/logs/persistence-restart.md)로 확인했다.
- JSON 적용 후 추가 퀴즈: 추가·종료·재실행 후 목록에 남는 원본 로그는 아직
  확보하지 않았다. 이 항목까지 확인하기 전에는 전체 영속성 완료로 표시하지 않는다.

## JSON 스키마

```json
{
  "quizzes": [
    {
      "category": "과학",
      "question": "문제 내용",
      "choices": ["선택지 1", "선택지 2", "선택지 3", "선택지 4"],
      "answer": 1
    }
  ],
  "best_scores": {
    "과학": 80
  }
}
```

`quizzes`는 퀴즈 객체 목록이고 `best_scores`는 카테고리 이름을 키로 사용하는
0~100점 정수 최고 점수다. `category`와 `question`은 비어 있지 않은 문자열,
`choices`는 정확히 4개의 문자열, `answer`는 1~4 정수여야 한다.

## 손상 파일 복구

손상된 JSON이나 잘못된 스키마를 발견하면 원인을 출력하고, 원본을
`상태파일명.corrupt-YYYYMMDD-HHMMSS-ffffff`로 복사한 뒤 기본 퀴즈와 빈
점수로 활성 상태 파일을 복구한다.

사용자가 확인용 파일의 `quizzes` 키를 `quizes`로 바꿔 직접 실행했을 때
`quizzes는 목록이어야 합니다.`가 출력됐고,
`state.test.json.corrupt-20260805-181939-287895`가 만들어진 뒤 기본 데이터로
복구됐다. 캡처와 해당 백업 파일의 실제 내용은
[JSON 복구 연결 기록](evidence/logs/json-recovery.md)에서 함께 확인할 수 있다.

## 파일 구조

```text
.
├── main.py
├── src/
│   ├── game_manager.py
│   ├── quiz.py
│   └── default_quizzes.py
├── tests/                     # 과거 개발 기록, 앞으로 실행·수정하지 않음
├── state.json                 # 실제 게임 상태, Git 추적
├── state.test.json            # 직접 확인용 상태, Git 제외
├── README.md
├── docs/
│   ├── architecture-plan.md
│   ├── requirements.md
│   ├── progress.md
│   ├── worklog.md
│   └── troubleshooting.md
└── evidence/
    ├── git/
    ├── logs/
    └── screenshots/
```

## 실행 및 작업 증거

| 범위 | 증거 | 설명 |
|---|---|---|
| 초기 환경·Git | [초기 Git 기록](evidence/git/git-verification.md), [화면](evidence/git/git-log.png) | 초기 설정 자료 |
| 메뉴 | [초기 메뉴 화면](evidence/screenshots/menu-test.png) | 기능 구현 초반 자료이며 최종 화면은 나중에 다시 정리 |
| 퀴즈 목록 | [목록 화면](evidence/screenshots/quiz-list.png) | 가로형 선택지와 문제 간격 확인 |
| 최고 점수 | [직접 실행 원본 로그](evidence/logs/best-score.md) | JSON 연결 전 점수 계산·조회 흐름 |
| 최고 점수 영속성 | [재실행 원본 로그](evidence/logs/persistence-restart.md) | 확인용 JSON에서 100점 저장 후 재실행 복원 |
| 안전 종료 | [원본 로그](evidence/logs/safe-exit.md), [화면](evidence/screenshots/safe-exit.png) | Ctrl+C·EOF 처리 |
| JSON 복구 | [연결 기록](evidence/logs/json-recovery.md), [화면](evidence/screenshots/json-recovery.png) | 오류 원인, 백업 파일명·내용, 기본 복구 연결 |
| 과거 병합 | [병합 화면](evidence/screenshots/git-merge.png) | 개발 과정 자료; 최종 그래프는 모든 작업 후 다시 확보 |

퀴즈 추가 영속성·플레이 결과·최종 Git 그래프·clone/pull·최종
검증 증거는 아직 남아 있다. Git 이력과 메뉴 최종 증거는 모든 기능과 병합이
끝난 뒤 한 번에 정리한다.

## Git 작업 상태

- 원격 저장소: <https://github.com/naktaa/Codyssey-E1-2-python-quiz>
- 기본 브랜치: `main` — `533b98f`
- 현재 통합 브랜치: `main`
- JSON 병합: `4984e31 Merge: JSON 상태 관리 브랜치 병합`
- JSON 관련 커밋: `45990d1`, `40fdea5`, `103a3b1`
- `feature/solving` 작업과 `main` 병합 기록은 이미 존재
- 최종 그래프와 clone·pull 기록은 마지막 단계에서 정리

## 상세 문서

- [아키텍처와 구현 기준](docs/architecture-plan.md)
- [요구사항 추적표](docs/requirements.md)
- [현재 진행 상태](docs/progress.md)
- [날짜별 작업 기록](docs/worklog.md)
- [문제 해결 기록](docs/troubleshooting.md)

## 남은 필수 작업

- [x] 직접 작성한 기본 퀴즈 5개 반영
- [x] 확인용 상태에서 최고 점수 저장 후 재실행 영속성 원본 로그 확보
- [x] JSON 기능을 `main`에 병합
- [ ] 추가·플레이·영속성 실행 증거 확보
- [ ] 최종 메뉴와 Git 그래프 증거 재정리
- [ ] 별도 디렉터리 clone·push 후 기존 폴더 pull 반영 확인
- [ ] macOS zsh에서 README 절차로 최종 직접 실행 검증
