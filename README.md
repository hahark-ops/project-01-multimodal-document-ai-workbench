# Document AI Workbench

텍스트 중심 PDF를 업로드하면 페이지별 텍스트를 파싱하고, chunk retrieval, grounded answer, summary, evaluation까지 한 흐름으로 확인할 수 있는 포트폴리오 프로젝트입니다. 저장소 이름의 `multimodal`은 장기 목표를 반영한 것이고, 현재 구현 범위는 `text-first PDF baseline`입니다.

## Current Status

- 상태: Phase 5 portfolio wrap-up 완료
- 시작일: 2026-03-13
- 대상: AWS AI School 포트폴리오 프로젝트
- 현재 기준: providerless baseline 기준의 end-to-end demo 가능

## What This Project Demonstrates

- 문서 AI 문제를 작은 vertical slice로 나누어 구현하는 방식
- PDF parsing -> retrieval -> grounded answer -> summary -> evaluation으로 이어지는 흐름 설계
- "그럴듯한 답변"보다 "근거를 찾고 연결하는 구조"를 먼저 만드는 접근
- GitHub 문서화와 작업 로그를 통해 구현 과정과 판단 근거를 남기는 방식

## End-to-End Flow

1. PDF를 업로드한다.
2. PyMuPDF로 페이지별 텍스트를 추출한다.
3. 문서 텍스트를 chunk 단위로 나누고 로컬 인덱스를 만든다.
4. 질문을 입력하면 top-k retrieval 결과와 grounded answer를 함께 확인한다.
5. 문서 summary와 evaluation suite 결과를 한 화면에서 확인한다.

## Implemented Scope

### Phase 1

- `POST /documents/upload`
- `GET /documents/{document_id}`
- 로컬 PDF 저장
- 페이지별 텍스트 추출
- 업로드 및 파싱 결과 UI

### Phase 2

- `GET /documents/{document_id}/chunks`
- `POST /retrieval/search`
- chunk metadata 저장
- 로컬 on-disk vector index
- retrieval playground UI

### Phase 3

- `POST /answers/ask`
- extractive grounded answer baseline
- citation과 page number 표시
- retrieval / grounded answer 비교 UI

### Phase 4

- `POST /summaries/generate`
- `POST /evaluations/run`
- extractive summary baseline
- bundled evaluation suite
- summary / evaluation scorecard UI

## Demo Screens

### Retrieval And Grounded Answer

![Retrieval and grounded answer demo](docs/assets/phase5-answer-panel.png)

### Summary And Evaluation

![Summary and evaluation demo](docs/assets/phase5-evaluation-panel.png)

## Baseline Evidence

2026-03-13 기준 로컬 데모 실행 결과입니다. 이 수치는 `단일 샘플 계약 문서 + 5개 번들 질문` 기준의 controlled baseline evidence입니다.

- evaluation suite: `nc_dac_sample_contract_v1`
- question count: `5`
- retrieval hit rate: `100%`
- citation hit rate: `100%`
- answer keyword hit rate: `100%`
- overall pass rate: `100%`

즉, 현재 구현이 end-to-end로 동작한다는 근거로는 충분하지만, 모든 문서 유형에 일반화된 품질을 보장하는 수치는 아닙니다.

상세 결과와 해석은 [docs/RESULTS.md](docs/RESULTS.md)에 정리했습니다.

## Technical Direction

- Frontend: Next.js
- Backend: FastAPI
- Parsing: PyMuPDF
- Storage: local PDF + JSON metadata
- Retrieval: local on-disk vector index
- Answer / Summary: providerless extractive baseline
- Evaluation: bundled question suite + deterministic metric calculation

이 방향을 먼저 택한 이유는 외부 모델 비용과 인프라 복잡도를 늘리기 전에, 문서 처리 흐름과 근거 연결 구조를 먼저 검증하기 위해서입니다.

## Repository Map

- 프로젝트 개요: [README.md](README.md)
- 설계 기준: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 실행 계획: [docs/PLAN.md](docs/PLAN.md)
- 작업 기록: [docs/WORKLOG.md](docs/WORKLOG.md)
- 데모 결과와 해석: [docs/RESULTS.md](docs/RESULTS.md)
- 발표 / 면접 포인트: [docs/TALKING_POINTS.md](docs/TALKING_POINTS.md)

## Why The Baseline Is Useful

- retrieval과 answer를 분리해서 볼 수 있다.
- citation 구조를 먼저 고정해서 이후 LLM 교체가 쉬워진다.
- 작은 평가셋으로 현재 강점과 약점을 빠르게 기록할 수 있다.
- 포트폴리오 관점에서 "무엇을 만들었는지"보다 "왜 이렇게 순서를 잡았는지"를 설명하기 좋다.

## Known Limitations

- 현재 검증 범위는 텍스트 중심 PDF baseline에 한정된다.
- OCR, 표 복원, 이미지 설명 생성은 아직 구현하지 않았다.
- answer와 summary는 extractive baseline이라 자연스러운 생성 품질은 제한적이다.
- evaluation은 keyword 중심의 baseline이라 의미적 정답 판정까지는 하지 않는다.
- 외부 vector store, cloud storage, deployment는 아직 붙이지 않았다.

## Suggested Next Extensions

- OCR 추가로 스캔 PDF 대응
- OpenAI 또는 Bedrock 기반 answer / summary 고도화
- Qdrant 또는 pgvector 기반 retrieval 실험
- S3 저장과 배포 환경 연결
- 문서 유형 확장과 평가셋 다양화

## Verification

- backend: `uv run pytest`
- frontend: `npm run build`
