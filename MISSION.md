# E1-2 나만의 퀴즈 게임 미션

## 1. 미션 목적

Python 기본 문법, 객체 지향 구조, JSON 파일 입출력, 예외 처리와 Git 워크플로우를 사용해 터미널 기반 퀴즈 게임을 완성한다. 프로그램의 동작뿐 아니라 구현 과정, 브랜치 병합, clone·pull 실습과 실행 증거까지 제출 가능한 형태로 정리한다.

## 2. 필수 최종 산출물

- Python 3.10 이상에서 실행되는 콘솔 퀴즈 게임
- 최소 2개 클래스: `Quiz`, `GameManager`
- 직접 작성한 동일 주제 퀴즈 5개 이상
- 프로젝트 루트의 UTF-8 `state.json`
- 퀴즈와 최고 점수의 재실행 후 유지
- 잘못된 입력, `KeyboardInterrupt`, `EOFError`, 파일 없음·손상 처리
- GitHub 공개 저장소 URL
- 의미 있는 커밋 10개 이상
- 추가 브랜치 생성·작업·병합 기록 1회 이상
- `init`, `add`, `commit`, `push`, `pull`, `checkout`, `clone` 사용 기록
- 필수 항목을 포함한 `README.md`
- 개발 환경, 주요 기능, Git 그래프 실행 화면 증거

## 3. 필수 기능

1. 메뉴 표시 및 기능 선택
2. 퀴즈 풀기
3. 퀴즈 추가
4. 퀴즈 목록 보기
5. 최고 점수 확인
6. 종료
7. 숫자 입력 공통 검증
8. 안전 종료와 가능한 범위의 저장
9. JSON 저장·불러오기 및 복구

## 4. 권장 프로젝트 구조

```text
codyssey-e1-2-quiz-game/
├── main.py
├── quiz.py
├── game_manager.py
├── default_quizzes.py
├── state.json
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

구조는 권장안이며, 최소 클래스·기능 분리·루트 `state.json` 요구사항을 만족하면 다른 단순한 구조도 가능하다.

## 5. 권장 책임 분리

### `Quiz`

- 속성: `question`, `choices`, `answer`
- 퀴즈와 선택지 출력
- 사용자 답과 정답 비교
- JSON 저장용 딕셔너리 변환
- 딕셔너리에서 객체 복원

### `GameManager`

- 퀴즈 목록과 최고 점수 관리
- 메뉴 루프
- 숫자·문자열 입력 검증
- 퀴즈 플레이, 추가, 목록, 점수 확인
- `state.json` 저장·불러오기
- 안전 종료

### 진입점

- `main.py`는 `GameManager` 생성과 실행만 담당하도록 유지한다.

## 6. 데이터 스키마 권장안

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

- `answer`: 1~4 정수
- `best_score`: 아직 플레이하지 않았으면 `null`, 플레이 후 0~100 정수 점수 권장
- 실제 구현에서는 스키마를 한 번 정한 뒤 코드와 README에서 일관되게 사용한다.

## 7. 개발 단계

1. 저장소와 초기 문서 설정
2. 메뉴와 공통 입력 처리
3. `Quiz` 클래스
4. 기본 퀴즈 5개 이상
5. 별도 브랜치에서 퀴즈 풀기
6. `main` 병합
7. 퀴즈 추가
8. 퀴즈 목록
9. 점수 계산·갱신
10. `GameManager` 책임 정리
11. `state.json` 저장·불러오기와 오류 복구
12. 통합 예외 처리와 안전 종료
13. 전체 실행 검증 및 증거 수집
14. README 완성
15. 별도 디렉터리 clone → 변경 → commit → push → 기존 작업 폴더 pull
16. 최종 Git 그래프·재현 검증

## 8. Git 계획

### 권장 브랜치

- `main`: 통합·제출 브랜치
- `feature/quiz-play`: 퀴즈 풀기 기능 구현 브랜치

### 권장 커밋 흐름

1. `Chore: 프로젝트 초기 파일 구성`
2. `Feat: 메뉴와 공통 숫자 입력 처리 구현`
3. `Feat: Quiz 클래스 구현`
4. `Feat: 기본 퀴즈 데이터 추가`
5. `Feat: 퀴즈 출제와 결과 출력 구현` — 별도 브랜치
6. `Merge: 퀴즈 플레이 브랜치 병합` — 병합 방식에 따라 자동 메시지 가능
7. `Feat: 퀴즈 등록 기능 구현`
8. `Feat: 퀴즈 목록 조회 기능 구현`
9. `Feat: 최고 점수 계산과 조회 구현`
10. `Feat: state.json 저장과 불러오기 구현`
11. `Fix: 입력 중단과 손상 파일 복구 처리`
12. `Refactor: GameManager 기능별 책임 정리`
13. `Test: 필수 기능과 데이터 영속성 검증`
14. `Docs: README와 제출 증거 정리`
15. `Docs: clone 실습 확인 문구 추가` — 복제 디렉터리에서 수행 가능

최소 10개를 충족하되 실제 변경 단위에 맞춰 조정한다.

## 9. 증거 수집 계획

| 시점 | 확인 내용 | 권장 파일 |
|---|---|---|
| 초기 환경 확인 | `python3 --version`, `git --version`, VSCode 터미널 | `evidence/screenshots/env-python-git.png` |
| 메뉴 완료 | 메뉴와 잘못된 입력 복귀 | `evidence/screenshots/menu.png` |
| 퀴즈 추가 | 문제·선택지·정답 입력과 성공 메시지 | `evidence/screenshots/add-quiz.png` |
| 목록 확인 | 추가한 퀴즈가 목록에 표시 | `evidence/screenshots/quiz-list.png` |
| 플레이 완료 | 정답·오답과 최종 결과 | `evidence/screenshots/play-result.png` |
| 점수 확인 | 최고 점수 화면 | `evidence/screenshots/best-score.png` |
| 재실행 | 추가 퀴즈와 점수 유지 | `evidence/screenshots/persistence-restart.png` |
| Git 완료 | 브랜치 분기·병합과 커밋 10개 이상 | `evidence/screenshots/git-graph.png` |
| clone·pull | 복제본 push 후 기존 폴더 pull 반영 | `evidence/screenshots/clone-pull.png` |
| 최종 검증 | 주요 명령과 실제 출력 | `evidence/logs/final-verification.txt` |

## 10. README 필수 항목

- 프로젝트 개요
- 퀴즈 주제와 선정 이유
- 실행 환경과 실행 방법
- 기능 목록
- 파일 구조
- `state.json` 경로, 역할, 필드 구조
- 필요 시 실행 화면

## 11. 환경과 제약

- 교육장 macOS, zsh 기준으로 개발·실행·검증한다.
- Python 3.10 이상을 사용한다.
- 외부 라이브러리를 사용하지 않는다.
- 절대 경로를 코드에 하드코딩하지 않는다.
- UTF-8과 LF를 사용한다.
- 보너스 과제는 필수 요구사항 완료 후 진행한다.

## 12. 원문에서 결정이 필요한 부분

- 퀴즈 주제는 사용자가 선택해야 한다. 구현 전 README와 기본 데이터에 같은 주제를 반영한다.
- 최고 점수의 의미는 정답 수 또는 100점 환산 중 하나로 정하고 일관되게 사용한다. 이 문서는 0~100 점수 방식을 권장한다.
- 손상된 `state.json`의 복구 방식은 기본 데이터로 초기화하거나 별도 백업 후 초기화할 수 있다. 최소 요구는 안내와 정상 실행이다.
- 예시 화면의 문구·이모지·파일 경로는 참고이며 그대로 복사할 필수 조건이 아니다.

## 13. 제출을 막을 수 있는 조건

- 클래스가 2개 미만이거나 역할 분리가 없음
- 기본 퀴즈가 5개 미만
- `state.json`이 루트가 아니거나 재실행 시 데이터가 사라짐
- 잘못된 입력이나 Ctrl+C에서 traceback으로 종료됨
- 커밋이 10개 미만이거나 의미 없는 커밋으로 채움
- 실제 브랜치 작업·병합 기록이 없음
- clone 또는 pull 사용 증거가 없음
- README 필수 항목 누락
- 요구된 실행·Git 스크린샷 누락
- GitHub에 push되지 않았거나 저장소 URL 제출 누락
