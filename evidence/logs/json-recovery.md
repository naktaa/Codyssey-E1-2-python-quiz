# JSON 손상 파일 복구 연결 기록

- 수행일: 2026-08-05
- 실행 방식: 사용자 터미널 직접 실행
- 실행 대상: Git에서 제외한 확인용 `state.test.json`
- 화면 증거: [json-recovery.png](../screenshots/json-recovery.png)

## 터미널 캡처에 표시된 원문

아래 내용은 캡처에 표시된 실행 명령과 복구 출력이다.

```console
moneydon779498@c5r7s3 Codyssey-E1-2-python-quiz % QUIZ_STATE_MODE=test py
[테스트 모드] state.test.json을 사용합니다.
상태 파일이 손상되었습니다: quizzes는 목록이어야 합니다.
손상된 상태 파일을 백업했습니다: state.test.json.corrupt-20260805-181939-287895
기본 데이터로 상태 파일을 복구했습니다.

=== 상식 퀴즈 게임 ===
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록 보기
4. 카테고리별 최고 점수
5. 종료
```

## 화면과 백업 파일 연결

캡처에 출력된 파일명과 프로젝트 루트에 실제 생성된 파일명이 다음과 같이
일치한다.

```text
state.test.json.corrupt-20260805-181939-287895
```

이 파일은 복구 전 손상 원본이다. `quizzes`여야 할 최상위 키가 `quizes`로
기록되어 있었고, 나머지 퀴즈 데이터와 빈 최고 점수는 그대로 보존되어 있다.
아래는 해당 백업 파일에서 확인한 원문 전체다.

```json
{
  "quizes": [
    {
      "category": "과학",
      "question": "물의 화학식은 무엇인가요?",
      "choices": [
        "CO2",
        "H2O",
        "O2",
        "NaCl"
      ],
      "answer": 2
    },
    {
      "category": "과학",
      "question": "지구의 자연 위성은 무엇인가요?",
      "choices": [
        "태양",
        "화성",
        "달",
        "금성"
      ],
      "answer": 3
    },
    {
      "category": "역사",
      "question": "훈민정음을 창제한 왕은 누구인가요?",
      "choices": [
        "세종",
        "태조",
        "영조",
        "정조"
      ],
      "answer": 1
    },
    {
      "category": "역사",
      "question": "조선을 건국한 인물은 누구인가요?",
      "choices": [
        "이순신",
        "이성계",
        "강감찬",
        "장영실"
      ],
      "answer": 2
    }
  ],
  "best_scores": {}
}
```

## 복구 후 활성 파일

백업이 성공한 뒤 `state.test.json`은 기본 문제 4개와 빈 `best_scores`를 가진
정상 스키마로 다시 만들어졌다. 따라서 손상 원본은 위 백업 파일에 남고,
게임은 복구된 확인용 파일로 메뉴를 계속 실행했다.

## 같은 디렉터리의 이전 백업

점검 당시 프로젝트 루트에는 앞선 JSON 문법 오류 확인에서 만들어진 다음
파일도 남아 있었다.

```text
state.test.json.corrupt-20260805-181428-075032
```

이 파일의 실제 내용은 완성되지 않은 다음 두 줄이다.

```json
{
  "quizzes": [
```

두 백업 파일은 모두 `.gitignore`의 `state.test.json.corrupt-*` 규칙으로 Git
추적에서 제외된다. 이 문서는 화면에 나온 백업 파일명과 Git에 올라가지 않는
실제 손상 원본 내용을 함께 보존하기 위해 작성했다.
