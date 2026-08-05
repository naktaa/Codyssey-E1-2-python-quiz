# E1-2 나만의 퀴즈 게임

> 현재 상태: 카테고리별 플레이·목록, 메모리 기반 추가와 안전 종료 검증 완료

## 프로젝트 개요

터미널 메뉴에서 퀴즈 풀기, 퀴즈 추가, 목록 확인, 최고 점수 확인을 수행하는
Python 콘솔 프로그램을 구현한다. 현재는 퀴즈 풀기와 메모리 기반 추가까지
완료했으며, 최고 점수와 `state.json` 영속성은 다음 단계에서 구현한다.

## 퀴즈 주제와 선정 이유

- 퀴즈 주제: **여러 카테고리로 구성된 상식 퀴즈**
- 선정 이유: **다양한 분야의 지식을 카테고리별로 나누어 학습하고 확인하기 위해 선정**

현재는 플레이 확인용 과학·역사 임시 문제 4개를 사용한다. 최종 카테고리와
기본 문제 5개 이상은 사용자가 문제 데이터를 준비한 뒤 교체한다.

## 개발 환경

- OS: macOS
- Shell: zsh
- Python: 3.12.13 (요구 버전: 3.10 이상)
- Git: 2.53.0
- 외부 라이브러리: 사용하지 않음

2026-08-04 터미널에서 Python 3.12.13 자동 테스트 17개와 전체 컴파일을
다시 확인했다.

## 실행 방법

프로젝트 루트에서 Python 3.10 이상인지 확인한 뒤 실행한다.

```zsh
python --version
python main.py
```

현재 zsh의 `python` 별칭이 Python 3.12.13을 가리키는 환경에서 검증했다.
시스템 `/usr/bin/python3`는 3.9이므로 이 프로젝트 실행에 사용하지 않는다.

## 기능 목록

| 기능 | 설명 | 상태 |
|---|---|---|
| 메뉴 | 기능 번호 선택 및 종료 | 실행 검증 완료 |
| 공통 입력 검증 | 공백, 빈 입력, 문자, 범위 오류 처리 | 실행 검증 완료 |
| Quiz 데이터 모델 | 퀴즈 검증·출력·정답 확인·딕셔너리 변환 | 구현 완료 |
| 임시 기본 데이터 | 과학·역사 카테고리의 플레이 확인용 문제 4개 | 구현 중 |
| 퀴즈 풀기 | 카테고리 선택, 순차 출제, 정오답과 결과 출력 | 구현 완료 |
| 퀴즈 추가 | 현재 실행 목록에 등록하고 같은 실행에서 바로 플레이 | 실행 검증 완료 |
| 퀴즈 목록 | 카테고리별 문제와 가로형 선택지 출력 | 증거 확보 완료 |
| 최고 점수 | 플레이 결과 비교·갱신·조회 | 예정 |
| 데이터 저장 | `state.json`에 퀴즈와 점수 저장 | 예정 |
| 데이터 복구 | 파일 없음·손상·입출력 오류 처리 | 예정 |
| 안전 종료 | Ctrl+C, EOF 발생 시 traceback 없이 종료 | 실행 검증 완료 |

## 계획된 파일 구조

```text
.
├── main.py                     # 프로그램 진입점
├── src/                        # 애플리케이션 소스 코드
│   ├── __init__.py
│   ├── game_manager.py         # QuizGame 클래스와 게임 흐름
│   ├── quiz.py                 # Quiz 클래스
│   └── default_quizzes.py      # 임시 문제 4개, 최종 기본 퀴즈 5개 이상
├── tests/                      # 표준 라이브러리 unittest
├── state.json                  # 퀴즈와 최고 점수 저장
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

`main.py`와 `state.json`은 미션 실행·저장 기준에 맞춰 루트에 두고, 기능
코드는 `src/`, 자동 테스트는 `tests/`에서 관리한다.

## 데이터 파일 설명

- 경로: 프로젝트 루트의 `state.json`
- 인코딩: UTF-8
- 역할: 퀴즈 목록과 최고 점수 저장
- 현재 상태: 구현 전

확정 스키마:

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

| 필드 | 설명 |
|---|---|
| `quizzes` | 퀴즈 객체 목록 |
| `category` | 퀴즈 카테고리 문자열 |
| `question` | 문제 문자열 |
| `choices` | 4개의 선택지 문자열 목록 |
| `answer` | 1~4 정답 번호 |
| `best_scores` | 카테고리 이름을 키로 사용하는 0~100점 최고 점수 |

## Git 작업 계획

- 원격 저장소: <https://github.com/naktaa/Codyssey-E1-2-python-quiz>
- 기본 브랜치: `main` (`origin/main` 추적)
- 첫 커밋: `a4887e4 Chore: 프로젝트 초기 파일 구성`
- 기능 브랜치: `feature/solving` 작업 후 `cb4f9cb`에서 병합 완료
- 현재 `main` 커밋 수: 16개
- 최신 기능 커밋: `5d08e39 Feat: 퀴즈 목록 조회 기능 구현`
- 실험 브랜치: `feature/state-json`을 원격에 별도 보관
- 개발 완료 후 별도 디렉터리에서 clone·수정·push
- 기존 작업 디렉터리에서 pull 후 반영 확인

## 실행 및 제출 증거

현재 확보한 증거:

- [초기 Git 설정 명령과 결과](evidence/git/git-verification.md)
- [Python·Git 버전과 첫 커밋 상태](evidence/git/git-log.png)
- [메모리 기반 퀴즈 추가와 재실행 비교](evidence/logs/memory-persistence-test.md)
- `evidence/screenshots/menu-test.png`: 메뉴 예비 화면
- `evidence/screenshots/git-merge.png`: 브랜치 병합 예비 화면

예비 PNG에는 로컬 계정명과 호스트명이 표시되어 최종 제출 전 다시
촬영하거나 공개 범위를 확인해야 한다.

기능 구현과 실제 검증 후 아래 파일을 추가한다.

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

- 확정 아키텍처: [`docs/architecture-plan.md`](docs/architecture-plan.md)
- 전체 요구사항: [`docs/requirements.md`](docs/requirements.md)
- 현재 진행 상태: [`docs/progress.md`](docs/progress.md)
- 작업 기록: [`docs/worklog.md`](docs/worklog.md)
- 트러블슈팅: [`docs/troubleshooting.md`](docs/troubleshooting.md)

## 제출 전 체크리스트

- [x] Python 3.10 이상에서 실행 확인
- [ ] 기본 퀴즈 5개 이상
- [x] `Quiz`, `QuizGame` 클래스 확인
- [ ] 모든 메뉴 기능 확인
- [ ] 잘못된 입력과 중단 입력 처리 확인
- [ ] `state.json` 재실행 영속성 확인
- [x] 커밋 10개 이상 확인
- [x] 브랜치 분기·병합 확인
- [ ] init/add/commit/push/pull/checkout/clone 사용 확인
- [x] GitHub push와 저장소 URL 확인
- [ ] README 필수 항목 실제 내용으로 갱신
- [ ] 요구된 스크린샷과 로그 확보
- [ ] 개인정보·토큰·절대 경로 노출 점검
