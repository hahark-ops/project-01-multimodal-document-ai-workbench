# Architecture

Status: Baseline v0.5  
Last Updated: 2026-03-13

## 1. Product Goal

이 프로젝트의 1차 목표는 멀티모달 문서를 업로드하고, 근거 기반 질문응답과 요약을 제공하는 최소 동작 제품을 만드는 것입니다.

처음부터 모든 문서 유형과 고급 기능을 다루지 않고, 아래 순서로 범위를 확장합니다.

- 1단계: 텍스트 중심 PDF 파싱
- 2단계: 검색과 근거 제시
- 3단계: 요약 및 핵심 정보 추출
- 4단계: OCR과 평가 고도화

## 2. Phase 1 Scope

1차 구현에서는 아래 범위에 집중합니다.

- 업로드 가능한 문서 형식은 PDF만 허용
- 텍스트 중심 PDF 우선
- 페이지별 텍스트 추출
- 파싱 결과 화면 표시

이번 단계에서 하지 않는 것:

- retrieval
- grounded answer 생성
- 표 구조 정교한 복원
- 이미지 설명 자동 생성
- 협업 기능
- 복잡한 비동기 작업 큐

## 3. User Flow

1. 사용자가 PDF를 업로드한다.
2. 시스템이 문서를 파싱하고 페이지별 텍스트를 추출한다.
3. 이후 단계에서 텍스트를 chunk 단위로 나누고 검색 가능한 형태로 저장한다.
4. 이후 단계에서 사용자가 질문을 입력한다.
5. 이후 단계에서 시스템이 관련 chunk를 찾고, 답변과 근거 페이지를 함께 반환한다.

## 4. System Flow

```text
User
  -> Upload PDF
Frontend
  -> Backend API
Parser
  -> Page Text
Chunking
  -> Embedding / Index
Retriever
  -> Context
LLM
  -> Answer + Citation
Frontend
  -> Result View
```

## 5. Initial Technical Direction

현재 작업 기준의 baseline은 아래와 같습니다.

- Frontend: Next.js
- Backend: FastAPI
- Parsing: PyMuPDF
- Phase 1 Storage: 원본 PDF는 로컬 파일, 파싱 결과 메타데이터는 문서 id 기준 JSON 저장
- Phase 2 Retrieval Store: 문서 id 기준 chunk JSON + 로컬 on-disk vector index
- Phase 3 Answering: providerless extractive grounded answer baseline
- Phase 4 Summary/Evaluation: providerless extractive summary + bundled evaluation suite
- OCR: Tesseract를 후속 단계에 추가
- External Vector Store: Qdrant 또는 pgvector는 grounded answer 이후 확장 시점에 재검토
- Model Provider: OpenAI 또는 Bedrock은 extractive baseline 검증 후 확정

선정 이유:

- Python 생태계가 문서 파싱과 OCR에 유리하다.
- FastAPI는 API 문서화와 실험이 빠르다.
- Next.js는 포트폴리오 데모 화면 구성에 유리하다.
- 초기에는 복잡한 인프라보다 구현과 검증 속도가 더 중요하다.

## 6. Decisions To Lock Next

아래 항목은 아직 미정이지만, 언제 무엇을 기준으로 결정할지 정합니다.

| 항목 | 결정 시점 | 판단 기준 |
|------|-----------|-----------|
| 샘플 문서 유형 | 완료 | `NC DAC Sample Contract Template` 선택. 공개 가능 여부, 텍스트 중심 여부, 페이지 번호 확인 가능 여부 기준 통과 |
| Retrieval Baseline | 완료 | 외부 인프라 없이 반복 실험 가능한 로컬 on-disk vector index 선택 |
| Grounded Answer Baseline | 완료 | provider 의존성 없이 retrieval과 citation 흐름을 먼저 검증하는 extractive 방식 선택 |
| Summary/Evaluation Baseline | 완료 | providerless summary와 번들 평가셋으로 품질 기록을 먼저 남기는 방식 선택 |
| Model Provider | Phase 5 전 | API 사용성, 비용, AWS 확장성 |
| 장기 저장 방식 | Phase 2 시작 전 | 로컬 개발 편의성, 이후 S3 확장 가능성 |

### Phase 1 Selected Sample

- 문서: [NC DAC Sample Contract Template](https://www.dac.nc.gov/documents/files/sample-contract-template-0)
- 유형: 계약서 템플릿 PDF
- 분량: 2페이지
- 선택 이유:
  - 작고 단순해서 첫 업로드/파싱 검증에 적합
  - 조항 구조가 명확해서 페이지 단위 결과 확인이 쉽다.
  - 이후 contract-style 질문응답 예시로 확장하기 좋다.

## 7. Planned Components

### Implemented In Phase 1

- Frontend 문서 업로드 화면
- Frontend 파싱 결과 화면
- Backend 문서 업로드 API
- Backend 문서 상세 조회 API
- Backend PDF 파싱 서비스
- 로컬 PDF 저장
- JSON 기반 파싱 결과 저장

### Implemented In Phase 2

- Backend chunk 생성 로직
- Backend 문서별 chunk 조회 API
- Backend top-k retrieval API
- 로컬 on-disk vector index
- Frontend retrieval playground UI
- chunk preview 화면

### Implemented In Phase 3

- Backend grounded answer 생성 로직
- Backend 질문응답 API
- citation 데이터 구조
- Frontend grounded answer UI
- answer와 retrieval 비교 화면

### Implemented In Phase 4

- Backend summary 생성 로직
- Backend evaluation 실행 로직
- 요약 API
- evaluation API
- 번들된 평가 질문 세트
- Frontend summary / evaluation 패널

### Frontend

- 문서 업로드 화면
- 문서 상세 화면
- 질문응답 화면
- 요약 결과 화면

### Backend

- 문서 업로드 API
- 문서 파싱 서비스
- chunk 생성 로직
- 검색 / 질문응답 API
- 요약 API

### Data Layer

- 원본 파일 저장
- 페이지 텍스트 저장
- chunk 및 메타데이터 저장
- 검색용 벡터 저장

## 8. Core Data Objects

### Document

- id
- filename
- title
- status
- page_count
- created_at

### Page

- document_id
- page_number
- text

### Chunk

- document_id
- page_number
- chunk_index
- content
- embedding

### Answer

- question
- answer_text
- citations
- latency_ms

### Summary

- document_id
- summary_text
- key_points
- highlights
- latency_ms

### Evaluation

- suite_id
- document_id
- metrics
- cases

## 9. Storage Boundary For Phase 1

Phase 1에서는 저장 구조를 단순하게 가져갑니다.

- 원본 PDF: 로컬 파일 시스템 저장
- 파싱 결과: 문서 id 기준 JSON 저장
- chunk / embedding: 아직 저장하지 않음

이렇게 시작하는 이유는 업로드와 파싱 흐름을 먼저 안정화하기 위해서입니다.

권장 디렉터리 개념:

```text
storage/
├── uploads/
│   └── {document_id}.pdf
├── parsed/
│   └── {document_id}.json
└── chunks/
    └── {document_id}.json
```

## 10. Phase 1 API Contract

Phase 1에서는 아래 두 개의 API만 우선 정의합니다.

### `POST /documents/upload`

목적:
- PDF 파일을 업로드하고 파싱 결과를 바로 반환한다.

요청:
- `multipart/form-data`
- field: `file`

성공 응답 예시:

```json
{
  "document_id": "doc_001",
  "filename": "sample-contract-template.pdf",
  "status": "parsed",
  "page_count": 2,
  "pages": [
    {
      "page_number": 1,
      "char_count": 1240,
      "text_preview": "This contract is entered into..."
    },
    {
      "page_number": 2,
      "char_count": 980,
      "text_preview": "Either party may terminate..."
    }
  ]
}
```

실패 응답 예시:

```json
{
  "error": {
    "code": "UNSUPPORTED_FILE_TYPE",
    "message": "Only PDF files are supported in Phase 1."
  }
}
```

추가 에러 코드:

- `EMPTY_FILE`
- `PDF_PARSE_FAILED`
- `FILE_SAVE_FAILED`
- `PARSED_DOCUMENT_SAVE_FAILED`
- `PARSED_DOCUMENT_LOAD_FAILED`
- `VALIDATION_ERROR`

### `GET /documents/{document_id}`

목적:
- 저장된 파싱 결과를 다시 조회한다.

성공 응답 예시:

```json
{
  "document_id": "doc_001",
  "filename": "sample-contract-template.pdf",
  "status": "parsed",
  "page_count": 2,
  "pages": [
    {
      "page_number": 1,
      "char_count": 1240,
      "text": "Full page text..."
    },
    {
      "page_number": 2,
      "char_count": 980,
      "text": "Full page text..."
    }
  ]
}
```

실패 응답 예시:

```json
{
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "Document 'doc_001' was not found."
  }
}
```

## 11. Phase 1 Data Structure

Phase 1에서 필요한 최소 데이터 구조는 아래와 같습니다.

### Upload Result Summary

- `document_id`
- `filename`
- `status`
- `page_count`
- `pages[].page_number`
- `pages[].char_count`
- `pages[].text_preview`

### Parsed Document Detail

- `document_id`
- `filename`
- `status`
- `page_count`
- `pages[].page_number`
- `pages[].char_count`
- `pages[].text`

## 12. Quality Criteria

Phase 1 완성 기준은 아래와 같습니다.

- 텍스트 PDF 업로드가 실패 없이 동작한다.
- 파싱된 텍스트를 페이지 단위로 확인할 수 있다.
- 샘플 문서 1개 이상에서 데모가 가능하다.
- 데모 화면에서 업로드와 파싱 결과 확인 흐름이 보인다.

현재 저장소 기준 확인된 근거:

- 자동화 테스트로 업로드, 상세 조회, 파일 형식 검증, 빈 파일 검증, 404 응답 형식을 확인
- 프론트엔드 프로덕션 빌드 통과
- 샘플 문서 실데모 캡처는 포트폴리오 정리 단계에서 별도 기록 예정

최종 MVP의 품질 기준은 `docs/PLAN.md`를 따른다.

## 13. Phase 2 Retrieval Contract

Phase 2에서는 아래 두 개의 retrieval surface를 추가합니다.

### `GET /documents/{document_id}/chunks`

목적:
- 문서가 어떤 chunk로 분해되었는지 확인한다.

성공 응답 핵심:

- `document_id`
- `chunk_count`
- `chunks[].page_number`
- `chunks[].chunk_index`
- `chunks[].word_count`
- `chunks[].text_preview`

### `POST /retrieval/search`

목적:
- 질문에 대해 관련성이 높은 chunk를 top-k로 반환한다.

요청 핵심:

- `query`
- `document_id`
- `top_k`

성공 응답 핵심:

- `query`
- `document_id`
- `top_k`
- `results[].page_number`
- `results[].chunk_index`
- `results[].score`
- `results[].text`

Phase 2 baseline은 grounded answer를 생성하지 않고, retrieval 결과만 반환한다.

## 14. Phase 3 Grounded Answer Contract

Phase 3에서는 아래 grounded answer surface를 추가합니다.

### `POST /answers/ask`

목적:
- 질문과 관련된 retrieval 결과를 바탕으로 답변과 citation을 함께 반환한다.

요청 핵심:

- `question`
- `document_id`
- `top_k`
- `max_citations`

성공 응답 핵심:

- `question`
- `document_id`
- `answer_text`
- `answer_strategy`
- `top_k`
- `citations[].page_number`
- `citations[].chunk_index`
- `citations[].excerpt`
- `latency_ms`

Phase 3 baseline은 외부 LLM 없이 extractive grounded answer를 생성한다. 즉, retrieval로 찾은 근거 문장을 조합해서 답변을 만들고, citation 배열로 근거를 노출한다.

## 15. Phase 4 Summary And Evaluation Contract

Phase 4에서는 아래 두 개의 surface를 추가합니다.

### `POST /summaries/generate`

목적:
- 문서의 핵심 문장을 요약과 key point 형태로 반환한다.

응답 핵심:

- `document_id`
- `summary_text`
- `key_points`
- `highlights[].page_number`
- `highlights[].chunk_index`
- `highlights[].excerpt`
- `latency_ms`

### `POST /evaluations/run`

목적:
- 번들된 평가 질문 세트로 retrieval / grounded answer baseline을 점검한다.

응답 핵심:

- `suite_id`
- `document_id`
- `metrics.retrieval_hit_rate`
- `metrics.citation_hit_rate`
- `metrics.answer_keyword_hit_rate`
- `metrics.overall_pass_rate`
- `cases[].question`
- `cases[].passed`

Phase 4 baseline은 summary와 evaluation 모두 외부 모델 없이 동작한다.

## 16. Main Risks

- 문서 종류에 따라 파싱 품질 차이가 크다.
- retrieval이 맞아도 답변이 근거를 잘못 묶을 수 있다.
- OCR 단계가 들어가면 난도가 급격히 올라간다.
- extractive baseline은 자연스러운 답변 품질이 제한될 수 있다.
- evaluation keyword match는 정밀한 의미 평가지표가 아니라 baseline 확인용이다.

따라서 초기 성공 기준은 "텍스트 중심 PDF에서 업로드와 파싱 결과 확인 흐름이 안정적으로 보이는가"입니다.

## 17. Open Questions

- 외부 vector store를 Qdrant로 갈지, pgvector로 갈지
- hashed embedding baseline을 어떤 시점에 provider embedding으로 교체할지
- extractive grounded answer를 어떤 시점에 LLM grounded answer로 교체할지
- extractive summary를 어떤 시점에 abstractive summary로 교체할지
- 요약 기능을 retrieval 뒤에 붙일지, 독립 기능으로 먼저 만들지
