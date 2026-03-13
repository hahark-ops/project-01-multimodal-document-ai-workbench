# Architecture Draft

## 1. Goal

이 프로젝트의 1차 목표는 "멀티모달 문서를 업로드하고, 근거 기반으로 질문응답과 요약을 제공하는 최소 동작 제품"을 만드는 것입니다.

처음부터 모든 문서 유형과 고급 기능을 한 번에 구현하지 않고 아래 순서로 확장합니다.

- 1단계: 텍스트 중심 PDF 업로드, 파싱, 검색, 질문응답
- 2단계: 스캔 문서 OCR 추가
- 3단계: 표/이미지 설명, reranking, 평가 고도화

## 2. Initial Technical Decisions

### Frontend: Next.js

- 단일 페이지 대시보드와 업로드 UI를 만들기 좋다.
- React 기반이라 포트폴리오 설명이 쉽고 자료가 많다.
- 이후 배포와 확장이 비교적 편하다.

### Backend: FastAPI

- Python 생태계의 OCR, 문서 파싱, 임베딩 라이브러리와 연결이 쉽다.
- 비개발자 출발 프로젝트에서도 구조를 이해하기 상대적으로 쉽다.
- Swagger 기반 API 문서를 자동으로 제공할 수 있다.

### Parsing: PyMuPDF

- PDF에서 텍스트와 페이지 단위 정보를 빠르게 추출하기 좋다.
- 초기 MVP에서 "페이지 번호 기반 근거 표기"를 구현하기 유리하다.

### OCR: Tesseract

- 스캔 문서 대응을 위한 2단계 도입 도구다.
- 처음부터 OCR 품질 최적화보다 "OCR 파이프라인 연결"을 먼저 확인하는 데 적합하다.

### Vector Store: Qdrant

- 벡터 검색 용도가 명확하고 로컬 개발이 비교적 단순하다.
- 메타데이터 필터링과 검색 실험을 하기에 적절하다.

### Model Provider Strategy

- LLM/Embedding 호출부는 추상화해서 OpenAI와 Bedrock 중 하나를 교체 가능하게 설계한다.
- 초기 개발은 가장 빠르게 검증 가능한 provider로 시작하고, 이후 AWS 연동을 추가한다.

## 3. High-Level Flow

```text
[User Upload]
    ->
[Next.js Frontend]
    ->
[FastAPI API]
    ->
[Document Parser / OCR]
    ->
[Chunking + Metadata Builder]
    ->
[Embedding Generator]
    ->
[Qdrant Index]

[User Question]
    ->
[Next.js Frontend]
    ->
[FastAPI API]
    ->
[Retriever]
    ->
[Optional Reranker]
    ->
[LLM Answer Generator]
    ->
[Answer + Citation(Page, Chunk)]
```

## 4. Main Components

### 4.1 Frontend

- 문서 업로드 화면
- 업로드한 문서 목록 화면
- 문서별 요약 및 질문응답 화면
- 답변 근거 페이지 번호와 문단 표시

### 4.2 Backend API

- 파일 업로드 처리
- 문서 파싱 및 인덱싱 작업 시작
- 문서 목록/상세 조회
- 문서 질문응답 및 요약 API
- 평가용 API 또는 내부 스크립트 연결

### 4.3 Parsing Pipeline

- PDF 텍스트 추출
- 페이지 정보 저장
- 스캔 여부 판단
- 필요 시 OCR 수행
- 표/이미지 처리는 후속 단계에서 추가

### 4.4 Retrieval / Generation

- 문서를 chunk 단위로 분리
- chunk와 페이지 정보를 함께 저장
- 질문 시 top-k 검색
- 필요하면 reranking 적용
- 최종 답변에 근거 문단과 페이지 번호 연결

### 4.5 Evaluation

- 샘플 문서별 질문 세트 구성
- retrieval hit 여부 기록
- grounded answer 여부 기록
- latency 측정

## 5. Suggested Data Model

### Document

- `id`
- `filename`
- `title`
- `file_type`
- `page_count`
- `status`
- `created_at`

### DocumentChunk

- `id`
- `document_id`
- `page_number`
- `chunk_index`
- `content`
- `modality`
- `metadata`

### QAResponse

- `question`
- `answer`
- `citations`
- `latency_ms`

### EvalCase

- `document_id`
- `question`
- `expected_pages`
- `expected_keywords`
- `result`

## 6. Initial API Plan

- `POST /documents/upload`
- `GET /documents`
- `GET /documents/{document_id}`
- `POST /documents/{document_id}/index`
- `POST /documents/{document_id}/ask`
- `POST /documents/{document_id}/summarize`
- `GET /health`

처음에는 비동기 작업 큐 없이 시작하고, 필요해지면 background task 또는 worker 구조를 추가합니다.

## 7. Repository Structure

```text
.
├── backend/
│   ├── app/
│   └── tests/
├── data/
│   └── samples/
├── docs/
├── frontend/
│   ├── app/
│   └── components/
├── infra/
└── scripts/
```

### Directory Purpose

- `frontend`: 업로드 UI, 문서 목록, Q&A 화면
- `backend`: FastAPI 서버, 파싱, 인덱싱, 질의응답 로직
- `docs`: 아키텍처, 작업 기록, 실험 결과 문서
- `data/samples`: 공개 가능한 샘플 문서 설명 또는 예시
- `infra`: Docker Compose, 배포 설정
- `scripts`: 평가, 데이터 정리, 개발 보조 스크립트

## 8. Development Strategy

### Phase 1

- 텍스트 중심 PDF 1~2개로 업로드와 파싱 성공
- chunk 저장 및 검색
- 근거 페이지 번호를 포함한 단순 Q&A 구현

### Phase 2

- OCR 문서 추가
- 스캔 문서에 대한 품질 확인
- 요약 및 핵심 항목 추출 추가

### Phase 3

- reranking 또는 retrieval 개선
- 평가셋 구성
- latency / quality 지표 기록

## 9. Sample Documents Strategy

초기 샘플 문서는 아래 범위에서 고릅니다.

- 공개 취업공고 PDF
- 개인정보가 제거된 계약서 템플릿
- 직접 만든 사내 보고서 형태의 PDF

실제 개인정보, 회사 내부 문서, 민감 정보는 저장소에 올리지 않습니다.

## 10. Key Risks

- 파싱 품질이 문서 유형마다 크게 다를 수 있다.
- 검색은 맞지만 답변이 근거를 잘못 묶을 수 있다.
- OCR 단계가 들어가면 구현과 디버깅 난도가 급격히 올라간다.

이 때문에 초기 완성 기준은 "텍스트 중심 PDF에서 근거 기반 답변이 동작하는가"로 잡습니다.
