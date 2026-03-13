# Work Log

이 문서는 실제로 무엇을 했는지, 왜 그렇게 결정했는지, 다음에는 무엇을 할지를 기록하는 진행 로그입니다.

## Logging Rule

각 기록은 아래 형식을 따릅니다.

```md
## YYYY-MM-DD - 작업 제목

### 목표
- 이번 작업의 목적

### 변경 사항
- 실제로 바뀐 내용

### 배운 점 / 이슈
- 시행착오, 판단 근거, 막힌 점

### 다음 단계
- 이어서 할 일
```

## 2026-03-13 - 저장소 재시작 및 문서 체계 재구성

### 목표
- 기존 뼈대를 모두 제거하고, 계획 중심의 문서 4개 체계로 다시 시작한다.

### 변경 사항
- 이전에 만든 코드와 보조 파일을 삭제했다.
- 저장소를 `README + ARCHITECTURE + WORKLOG + PLAN` 구조로 재구성했다.
- 이번 저장소의 시작 기준을 "구현 전 계획 명확화"로 다시 설정했다.

### 배운 점 / 이슈
- 초반에 구조를 너무 빨리 키우면 진행은 빨라 보이지만 방향이 흔들릴 수 있다.
- 포트폴리오 프로젝트에서는 코드 양보다 문제 정의, 범위 조절, 기록 방식이 먼저 정리되어야 한다.
- 이전 구조를 버린 이유는 "이미 구현을 시작한 것처럼 보이는 저장소"보다 "지금 무엇을 만들려는지 명확한 저장소"가 더 중요하다고 판단했기 때문이다.
- 이번에는 README는 소개, ARCHITECTURE는 설계, WORKLOG는 기록, PLAN은 실행 기준으로 역할을 분리해서 관리한다.

### 다음 단계
- 샘플 문서 유형을 정한다.
- 1차 구현 범위를 텍스트 중심 PDF로 고정한다.
- 첫 vertical slice를 시작한다.

## 2026-03-13 - Phase 1 실행 계획 구체화

### 목표
- 다음 구현 단계가 문서 수준이 아니라 실제 작업 단위로 보이게 만든다.

### 변경 사항
- `docs/PLAN.md`에 Phase 1 실행 순서 추가
- `docs/PLAN.md`에 Task Checklist 추가
- `docs/PLAN.md`에 추천 이슈 분해안 추가
- 샘플 문서 후보 우선순위 추가

### 배운 점 / 이슈
- 계획 문서는 단계 이름만 있어서는 부족하고, 다음 커밋에서 무엇이 생길지 보여줘야 한다.
- 구현 전에 저장 방식, 입력/출력 형식, 샘플 문서를 먼저 고정하면 이후 흔들림이 줄어든다.

### 다음 단계
- 샘플 문서 1개를 실제로 확정한다.
- 업로드 / 파싱 API 계약을 문서로 정리한다.
- 첫 vertical slice 구현을 시작한다.

## 2026-03-13 - 샘플 문서 선정

### 목표
- Phase 1에서 실제로 사용할 기준 문서를 1개 확정한다.

### 변경 사항
- 첫 기준 문서로 [NC DAC Sample Contract Template](https://www.dac.nc.gov/documents/files/sample-contract-template-0)를 선택했다.
- 백업 후보로 Wells Fargo 2024 Annual Report, IDACORP Annual Reports를 기록했다.
- README, ARCHITECTURE, PLAN에 선택 결과를 반영했다.

### 배운 점 / 이슈
- 첫 문서는 "실제 업무와 비슷한 문서"이면서도 "작고 단순한 문서"가 유리하다.
- 그래서 긴 보고서보다 먼저 짧은 계약서 템플릿을 선택하는 편이 vertical slice 속도와 안정성에 유리하다.

### 다음 단계
- 업로드 / 파싱 API 계약을 문서로 정리한다.
- 파싱 결과 데이터 구조를 정의한다.
- 첫 vertical slice 구현을 시작한다.

## 2026-03-13 - Phase 1 API 계약 정의

### 목표
- 구현 전에 저장 방식과 API 형식을 고정해서 다음 작업 범위를 명확히 한다.

### 변경 사항
- Phase 1 저장 방식을 `로컬 PDF + JSON 파싱 결과 저장`으로 확정했다.
- `POST /documents/upload`, `GET /documents/{document_id}` 두 개의 최소 API를 정의했다.
- 업로드 요약 응답과 상세 조회 응답의 데이터 구조를 정리했다.

### 배운 점 / 이슈
- 작은 프로젝트라도 입력 형식과 응답 형식을 먼저 정해 두면 구현이 훨씬 빨라진다.
- Phase 1에서는 full-text retrieval보다 `업로드 후 무엇을 반환할지`를 먼저 명확히 하는 편이 중요하다.

### 다음 단계
- 결과 확인 화면 또는 API 출력 형태를 더 구체화한다.
- 첫 vertical slice 구현을 시작한다.

## 2026-03-13 - Phase 1 vertical slice 구현

### 목표
- 문서에서 정의한 Phase 1 범위를 실제 코드로 구현하고 검증한다.

### 변경 사항
- `backend`에 FastAPI 기반 업로드 / 파싱 / 상세 조회 API 추가
- PDF를 로컬에 저장하고 파싱 결과를 JSON으로 저장하도록 구현
- PyMuPDF 기반 페이지별 텍스트 추출 로직 추가
- `frontend`에 Next.js 기반 업로드 UI와 결과 확인 화면 추가
- `.gitignore`, 환경 변수 예시, 패키지 설정 파일 추가

### 배운 점 / 이슈
- 문서에서 저장 방식과 API 계약을 먼저 정해둔 것이 실제 구현 속도를 높였다.
- Phase 1에서는 retrieval보다 업로드 후 결과를 얼마나 명확히 보여주느냐가 더 중요했다.
- 최소 검증 루프를 먼저 맞춘 뒤 다음 단계로 넘어가는 방식이 안정적이었다.

### 검증
- backend: `uv run pytest` 통과
- frontend: `npm run build` 통과

### 다음 단계
- chunk 데이터 구조를 정의한다.
- retrieval 기준 메타데이터를 설계한다.
- Vector Store 선택과 Phase 2 시작 조건을 확정한다.

## 2026-03-13 - Phase 1 검수 반영

### 목표
- 구현 직후 문서와 코드의 불일치를 줄이고, 검증 근거를 더 명확히 남긴다.

### 변경 사항
- README, PLAN, ARCHITECTURE의 Phase 1 상태 표현을 구현 완료 기준으로 정리했다.
- ARCHITECTURE에 실제 에러 코드와 `GET /documents/{document_id}` 실패 응답 예시를 추가했다.
- backend 테스트에 빈 파일 업로드와 없는 문서 조회 케이스를 추가했다.
- backend에서 업로드 저장 실패와 손상된 JSON 조회 실패를 구조화된 API 에러로 처리하도록 수정했다.
- frontend에서 비로컬 환경의 API 주소 누락을 명시적 오류로 처리하고, 응답 shape 검증을 추가했다.

### 배운 점 / 이슈
- 구현이 끝났다고 해서 곧바로 "증명까지 끝난 상태"는 아니다.
- 포트폴리오 저장소에서는 기능 구현, 자동화 검증, 데모 기록을 구분해서 써두는 편이 신뢰도가 높다.
- 작은 프로젝트라도 에러 응답 형식을 문서와 테스트 양쪽에 남겨두면 이후 프론트엔드 작업이 훨씬 수월하다.
- 멀티에이전트 검수는 "겉보기에는 돌아가지만 경계면에서 깨질 수 있는 부분"을 찾는 데 특히 유용했다.

### 다음 단계
- Phase 2를 위해 chunk 구조와 retrieval 기준 메타데이터를 정의한다.
- 샘플 문서 기준의 실제 데모 캡처를 추후 포트폴리오 정리 단계에서 남긴다.

## 2026-03-13 - Phase 2 retrieval foundation 구현

### 목표
- 파싱된 문서를 chunk 단위로 저장하고, 질문에 대해 관련 chunk를 찾는 baseline retrieval을 만든다.

### 변경 사항
- backend에 chunk 생성 로직과 로컬 on-disk vector index를 추가했다.
- `GET /documents/{document_id}/chunks`, `POST /retrieval/search` API를 구현했다.
- 업로드 시 문서를 자동으로 chunking하고 chunk metadata를 JSON으로 저장하도록 연결했다.
- frontend에 chunk preview와 retrieval 결과를 확인할 수 있는 playground UI를 추가했다.
- Phase 2 상태를 README, PLAN, ARCHITECTURE에 반영했다.

### 배운 점 / 이슈
- 검색 품질을 바로 완벽하게 만드는 것보다, 먼저 chunk 구조와 검색 인터페이스를 고정하는 편이 다음 단계 진행이 빠르다.
- 외부 벡터 저장소나 임베딩 API를 바로 붙이기 전에 로컬 baseline을 만들면 테스트와 반복 실험이 쉬워진다.
- Phase 2에서는 "정답 생성"보다 "관련 근거를 먼저 잘 찾는 구조"를 만드는 것이 핵심이었다.

### 검증
- backend: `uv run pytest` 통과
- frontend: `npm run build` 통과

### 다음 단계
- Phase 3를 위해 질문응답 API 계약을 정의한다.
- citation 구조와 답변 포맷을 고정한다.
- retrieval 결과를 바탕으로 grounded answer를 생성하는 흐름을 설계한다.

## 2026-03-13 - Phase 3 grounded answer 구현

### 목표
- retrieval 결과를 바탕으로 답변과 citation을 함께 반환하는 grounded answer baseline을 만든다.

### 변경 사항
- backend에 `POST /answers/ask` API를 추가했다.
- retrieval 결과에서 문장을 추출해 답변을 구성하는 extractive grounded answer 로직을 구현했다.
- citation 구조와 latency 필드를 응답에 포함했다.
- frontend에 grounded answer와 citation을 함께 보는 UI를 추가했다.
- Phase 3 상태를 README, PLAN, ARCHITECTURE에 반영했다.

### 배운 점 / 이슈
- 외부 LLM을 바로 붙이지 않아도 grounded answer의 핵심은 `답변 + 근거 연결 구조`를 먼저 만드는 데 있다.
- extractive baseline은 답변 자연스러움은 제한되지만, citation 검증과 API 계약 고정에는 유리하다.
- retrieval과 answer를 같은 화면에서 비교하니 검색 품질과 답변 품질을 분리해서 보기 쉬워졌다.

### 검증
- backend: `uv run pytest` 통과
- frontend: `npm run build` 통과

### 다음 단계
- Phase 4를 위해 summary API와 평가 질문 세트를 정의한다.
- retrieval / grounded answer 품질을 질문 세트 기준으로 점검한다.
- 포트폴리오용 데모 캡처와 실패 사례 기록을 보강한다.

## 2026-03-13 - Phase 4 summary and evaluation 구현

### 목표
- 문서 요약과 최소 평가 체계를 추가해서 품질 지표와 실패 지점을 저장소 안에 남긴다.

### 변경 사항
- backend에 `POST /summaries/generate`, `POST /evaluations/run` API를 추가했다.
- extractive summary baseline과 key point 추출 로직을 구현했다.
- NC DAC sample contract 기준 평가 질문 세트와 품질 지표 계산 로직을 추가했다.
- frontend에 summary 패널과 evaluation scorecard UI를 추가했다.
- README, PLAN, ARCHITECTURE에 Phase 4 상태와 계약을 반영했다.

### 배운 점 / 이슈
- 포트폴리오 관점에서는 "잘 답한다"보다 "어디까지 자동 평가했고, 어떤 기준으로 봤는가"를 남기는 것이 중요하다.
- evaluation 지표는 아직 정밀한 의미 평가는 아니지만, retrieval / citation / keyword 기준으로 baseline 상태를 빠르게 확인하는 데 유용하다.
- summary와 evaluation을 같은 화면에 두니 사용자 기능과 품질 점검 흐름이 자연스럽게 이어졌다.

### 검증
- backend: `uv run pytest` 통과
- frontend: `npm run build` 통과

### 다음 단계
- Phase 5로 넘어가서 데모 캡처, 품질 해석, 실패 사례, 최종 README 정리를 진행한다.
- evaluation 결과를 읽고 어떤 질문이 약한지 포트폴리오 관점에서 해석한다.

## 2026-03-13 - Phase 5 portfolio wrap-up

### 목표
- 구현 결과를 포트폴리오 관점에서 읽히는 형태로 정리하고, 실제 데모 증빙과 결과 해석을 저장소 안에 남긴다.

### 변경 사항
- README를 포트폴리오용 구조로 전면 정리했다.
- demo capture 이미지를 `docs/assets`에 추가했다.
- `docs/RESULTS.md`에 demo 흐름, baseline evaluation 결과, 해석, 실패 사례를 정리했다.
- `docs/TALKING_POINTS.md`에 발표 / 면접용 설명 포인트를 정리했다.
- PLAN과 ARCHITECTURE에 Phase 5 완료 상태와 baseline evidence를 반영했다.

### 배운 점 / 이슈
- 포트폴리오에서는 기능 목록보다 "무엇을 증명했고 무엇은 아직 증명하지 못했는가"를 구분해서 쓰는 편이 훨씬 중요하다.
- 100% pass rate 같은 숫자는 강해 보이지만, 어떤 문서와 어떤 평가셋 기준인지 함께 적지 않으면 오히려 신뢰도가 떨어질 수 있다.
- demo capture, 결과 해석, talking points를 분리해두니 저장소를 보는 사람과 면접에서 설명하는 사람 모두에게 쓰기 쉬워졌다.

### 검증
- 로컬 서버에서 PDF 업로드, retrieval, grounded answer, summary, evaluation까지 실제 실행
- baseline evaluation result 확인:
  - question count `5`
  - retrieval hit rate `100%`
  - citation hit rate `100%`
  - answer keyword hit rate `100%`
  - overall pass rate `100%`

### 다음 단계
- OCR, external vector store, LLM provider, deployment 중 어떤 확장을 먼저 할지 결정한다.
- 문서 유형을 늘려 evaluation suite를 다양화한다.
