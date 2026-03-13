# Talking Points

Status: Portfolio speaking notes  
Last Updated: 2026-03-13

## 1. One-Minute Introduction

이 프로젝트는 텍스트 중심 PDF 문서를 업로드하면 페이지별 텍스트를 파싱하고, retrieval, grounded answer, summary, evaluation까지 이어지는 문서 AI 워크벤치를 구현한 포트폴리오 프로젝트입니다. 핵심은 단순히 답변을 생성하는 것이 아니라, 어떤 페이지와 chunk를 근거로 답했는지 보여주는 구조를 먼저 만든 것입니다.

## 2. Why I Chose This Topic

- 실무 문서는 표, 조항, 스캔 이미지가 섞여 있어서 일반적인 챗봇보다 다루기 어렵다.
- 문서 AI는 "잘 말하는 것"보다 "정확한 근거를 찾는 것"이 더 중요하다고 판단했다.
- 그래서 처음부터 거대한 멀티모달 시스템을 만들기보다, 텍스트 중심 PDF에서 동작하는 작은 vertical slice부터 시작했다.

## 3. How I Broke The Problem Down

프로젝트를 한 번에 완성하려 하지 않고 5단계로 나눴다.

1. PDF 업로드와 파싱
2. chunk retrieval
3. grounded answer와 citation
4. summary와 evaluation
5. 포트폴리오 정리와 결과 해석

이렇게 나눈 이유는 각 단계마다 "무엇이 새로 가능해졌는지"를 GitHub 기록으로 남기기 위해서다.

## 4. Main Technical Choices

- frontend는 Next.js를 사용해 데모 UI를 빠르게 구성했다.
- backend는 FastAPI를 사용해 문서 처리 API를 빠르게 실험했다.
- parsing은 PyMuPDF를 사용해 텍스트 중심 PDF baseline을 먼저 검증했다.
- answer와 summary는 외부 LLM 대신 extractive baseline으로 시작했다.

이 선택의 핵심은 "모델 성능 과시"보다 "파이프라인 구조 검증"을 먼저 하자는 것이었다.

## 5. What I Can Show In Demo

- PDF 업로드 후 페이지별 텍스트 확인
- chunk preview와 retrieval 결과 확인
- grounded answer와 citation 확인
- summary와 evaluation scorecard 확인

현재 데모 기준에서는 `단일 샘플 계약 문서용 5개 질문 스위트`에서 retrieval, citation, answer keyword, overall pass가 모두 100%로 나온다. 다만 이 수치는 작은 aligned demo baseline 결과라는 점을 함께 설명해야 한다.

## 6. What I Learned

- retrieval이 answer보다 먼저 안정화되어야 전체 품질을 설명하기 쉽다.
- citation 구조를 먼저 고정하면 이후 LLM 교체가 쉬워진다.
- 포트폴리오 프로젝트에서는 구현 자체보다 범위 조절과 기록 방식이 중요하다.
- evaluation을 붙이고 나니 "잘 되는 점"보다 "어디까지 검증했는지"를 설명할 수 있게 됐다.

## 7. Honest Limitations

- 아직 OCR, 표 복원, 이미지 설명은 없다.
- extractive baseline이라 답변 표현이 자연스럽지 않을 수 있다.
- 평가가 keyword 중심이라 의미 평가까지는 하지 못한다.
- 지금 결과는 짧고 구조가 명확한 단일 계약서 스타일 샘플에 맞춰 검증한 상태다.

이 한계를 숨기기보다, 왜 이 범위에서 먼저 검증했는지 설명하는 것이 더 중요하다.

## 8. Good Interview Answer Frame

면접에서 설명할 때는 아래 순서가 깔끔하다.

1. 어떤 문제를 풀고 싶었는지
2. 왜 작은 vertical slice로 나눴는지
3. 각 phase에서 무엇을 구현했는지
4. 어떤 기준으로 품질을 점검했는지
5. 지금 한계와 다음 확장 방향이 무엇인지

## 9. Next Step Story

이 프로젝트의 다음 단계는 아래처럼 말할 수 있다.

- OCR을 붙여 스캔 문서까지 범위를 넓히겠다.
- OpenAI 또는 Bedrock을 붙여 answer와 summary 품질을 높이겠다.
- Qdrant 또는 pgvector를 붙여 retrieval 구조를 실제 서비스형에 가깝게 바꾸겠다.
- 평가셋을 계약서 외 다른 문서 유형으로 확장하겠다.
