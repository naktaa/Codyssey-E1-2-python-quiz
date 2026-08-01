# E1-2 나만의 퀴즈 게임

> 현재 상태: 초기 문서 구성 완료, 프로그램 구현 및 실행 검증 전

## 프로젝트 개요

터미널 메뉴에서 퀴즈 풀기, 퀴즈 추가, 목록 확인, 최고 점수 확인을 수행하는 Python 콘솔 프로그램이다. 퀴즈와 최고 점수는 프로젝트 루트의 `state.json`에 저장하여 프로그램을 다시 실행해도 유지하도록 구현할 예정이다.

## 퀴즈 주제와 선정 이유

- 퀴즈 주제: **TODO — 구현 전 확정**
- 선정 이유: **TODO — 본인이 해당 주제를 선택한 구체적인 이유 작성**

권장 예시: Python·Git 기초, 임베디드 시스템 기초, 좋아하는 영화·게임 등 직접 5문제 이상 설명할 수 있는 주제

## 개발 환경

- OS: macOS
- Shell: zsh
- Python: 3.10 이상
- 외부 라이브러리: 사용하지 않음

실제 검증 후 정확한 버전을 기록한다.

## 실행 방법

구현 후 프로젝트 루트에서 다음 명령으로 실행할 예정이다.

```zsh
python3 main.py
```

> 아직 프로그램 파일이 구현되지 않아 실행 미검증 상태이다.

## 기능 목록

| 기능 | 설명 | 상태 |
|---|---|---|
| 메뉴 | 기능 번호 선택 및 종료 | 예정 |
| 공통 입력 검증 | 공백, 빈 입력, 문자, 범위 오류 처리 | 예정 |
| 퀴즈 풀기 | 저장된 문제 출제, 정오답과 결과 출력 | 예정 |
| 퀴즈 추가 | 문제, 선택지 4개, 정답 번호 등록 | 예정 |
| 퀴즈 목록 | 저장된 문제 목록 출력 | 예정 |
| 최고 점수 | 플레이 결과 비교·갱신·조회 | 예정 |
| 데이터 저장 | `state.json`에 퀴즈와 점수 저장 | 예정 |
| 데이터 복구 | 파일 없음·손상·입출력 오류 처리 | 예정 |
| 안전 종료 | Ctrl+C, EOF 발생 시 저장 후 종료 | 예정 |

## 계획된 파일 구조

```text
.
├── main.py                 # 프로그램 진입점
├── quiz.py                 # Quiz 클래스
├── quiz_game.py            # QuizGame 클래스와 게임 흐름
├── default_quizzes.py      # 기본 퀴즈 5개 이상
├── state.json              # 퀴즈와 최고 점수 저장
├── README.md
├── AGENTS.md
├── MISSION.md
├── .gitignore
├── .gitattributes
├── docs/
│   ├── requirements.md
│   ├── progress.md
│   ├── worklog.md
│   └── troubleshooting.md
└── evidence/
    ├── screenshots/
    └── logs/
```

실제 구현 구조가 달라지면 검증 후 이 항목을 수정한다.

## 데이터 파일 설명

- 경로: 프로젝트 루트의 `state.json`
- 인코딩: UTF-8
- 역할: 퀴즈 목록과 최고 점수 저장
- 현재 상태: 구현 전

권장 스키마:

```json
{
  "quizzes": [
    {
      "question": "문제 내용",
      "choices": ["선택지 1", "선택지 2", "선택지 3", "선택지 4"],
      "answer": 1
    }
  ],
  "best_score": null
}
```

| 필드 | 설명 |
|---|---|
| `quizzes` | 퀴즈 객체 목록 |
| `question` | 문제 문자열 |
| `choices` | 4개의 선택지 문자열 목록 |
| `answer` | 1~4 정답 번호 |
| `best_score` | 아직 미플레이 시 `null`, 이후 최고 점수 |

## Git 작업 계획

- 기본 브랜치: `main`
- 기능 브랜치: `feature/quiz-play`
- 의미 있는 커밋 10개 이상
- 실제 브랜치 생성·작업·병합 수행
- 개발 완료 후 별도 디렉터리에서 clone·수정·push
- 기존 작업 디렉터리에서 pull 후 반영 확인

## 실행 및 제출 증거

실제 검증 후 아래 파일을 추가한다.

- `evidence/screenshots/env-python-git.png`
- `evidence/screenshots/menu.png`
- `evidence/screenshots/add-quiz.png`
- `evidence/screenshots/quiz-list.png`
- `evidence/screenshots/play-result.png`
- `evidence/screenshots/best-score.png`
- `evidence/screenshots/persistence-restart.png`
- `evidence/screenshots/git-graph.png`
- `evidence/screenshots/clone-pull.png`
- `evidence/logs/final-verification.txt`

## 요구사항과 진행 기록

- 전체 요구사항: [`docs/requirements.md`](docs/requirements.md)
- 현재 진행 상태: [`docs/progress.md`](docs/progress.md)
- 작업 기록: [`docs/worklog.md`](docs/worklog.md)
- 트러블슈팅: [`docs/troubleshooting.md`](docs/troubleshooting.md)

## 제출 전 체크리스트

- [ ] Python 3.10 이상에서 실행 확인
- [ ] 기본 퀴즈 5개 이상
- [ ] `Quiz`, `QuizGame` 클래스 확인
- [ ] 모든 메뉴 기능 확인
- [ ] 잘못된 입력과 중단 입력 처리 확인
- [ ] `state.json` 재실행 영속성 확인
- [ ] 커밋 10개 이상 확인
- [ ] 브랜치 분기·병합 확인
- [ ] init/add/commit/push/pull/checkout/clone 사용 확인
- [ ] GitHub push와 저장소 URL 확인
- [ ] README 필수 항목 실제 내용으로 갱신
- [ ] 요구된 스크린샷과 로그 확보
- [ ] 개인정보·토큰·절대 경로 노출 점검
