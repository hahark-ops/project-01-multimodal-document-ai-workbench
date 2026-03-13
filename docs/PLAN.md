# Project Plan

Status: Active  
Last Updated: 2026-03-13

## 1. Project Objective

포트폴리오에서 보여줄 수 있는 수준의 멀티모달 문서 AI 프로젝트를 완성한다. 핵심은 "문서를 올리고, 근거를 보여주며, 신뢰도 있게 답하는 흐름"을 직접 설계하고 구현했다는 점을 증명하는 것이다.

## 2. Success Definition

최종 MVP는 아래 조건을 만족하면 1차 성공으로 본다.

- 사용자가 PDF를 업로드할 수 있다.
- 파싱 결과를 화면에서 확인할 수 있다.
- 질문에 대해 관련 근거 페이지를 포함한 답변을 줄 수 있다.
- 최소한의 평가 기준과 결과 기록이 있다.
- README와 작업 로그만 읽어도 진행 과정이 이해된다.

측정 가능한 기준:

- 공개 가능한 샘플 문서 2종 이상 확보
- 각 문서에 대해 평가 질문 5개 이상 준비
- 질문응답 데모에서 근거 페이지 표시
- 최소 1개의 end-to-end 데모 시나리오 확보

## 3. Phase Breakdown

### Phase 0 - Planning Reset

목표:
- 저장소를 문서 중심으로 재정리한다.

완료 기준:
- README, ARCHITECTURE, WORKLOG, PLAN 작성 완료

상태:
- 완료

### Phase 1 - First Vertical Slice

목표:
- 업로드 → 파싱 → 결과 확인 흐름을 만든다.

작업:
- 샘플 PDF 선정
- 파일 업로드 처리
- 페이지별 텍스트 추출
- 파싱 결과 표시 화면 구성

Phase 1 Inputs:

- 공개 가능한 샘플 PDF 1개 이상
- 텍스트 중심 문서
- 페이지 번호를 확인할 수 있는 문서

Selected Sample:

- [NC DAC Sample Contract Template](https://www.dac.nc.gov/documents/files/sample-contract-template-0)
- 이유: 작고 단순하며 공개 가능하고, 텍스트 파싱 결과를 검증하기 쉽다.

Phase 1 Non-Goals:

- retrieval
- grounded answer
- 요약 기능
- OCR

Phase 1 Demo Definition:

- 사용자가 PDF를 업로드할 수 있다.
- 파싱 완료 후 페이지별 텍스트를 확인할 수 있다.
- 파일명, 페이지 수, 추출 여부가 화면에 보인다.

완료 기준:
- 한 개 이상의 PDF를 업로드하고 파싱 결과를 볼 수 있다.

상태:
- 구현 완료, 샘플 문서 데모 기록 보강 예정

Phase 1 Execution Order:

1. 샘플 문서 1개를 확정한다.
2. Phase 1 저장 방식을 `로컬 PDF + 문서 id 기준 JSON 저장`으로 고정한다.
3. 업로드 API와 파싱 API의 최소 응답 형식을 확정한다.
4. PDF 업로드와 페이지별 텍스트 추출 기능을 구현한다.
5. 결과를 확인할 수 있는 최소 화면 또는 API 응답을 만든다.
6. 샘플 문서 기준으로 데모와 기록을 남긴다.

### Phase 2 - Retrieval Foundation

목표:
- 파싱된 텍스트를 검색 가능한 구조로 만든다.

작업:
- chunking 기준 정의
- 메타데이터 구조 설계
- 벡터 저장소 연결
- top-k retrieval 확인

완료 기준:
- 질문 입력 시 관련 chunk를 안정적으로 찾을 수 있다.

### Phase 3 - Grounded Answer

목표:
- 검색 결과를 바탕으로 근거 기반 답변을 만든다.

작업:
- 질문응답 API 설계
- 답변 포맷 정의
- citation 구조 정의
- 페이지 번호와 문단 근거 표시

완료 기준:
- 답변과 함께 근거 페이지를 보여줄 수 있다.

### Phase 4 - Summary And Evaluation

목표:
- 요약 기능과 최소 평가 체계를 추가한다.

작업:
- 문서 요약 기능
- 핵심 정보 추출
- 평가 질문 세트 작성
- retrieval / grounded answer 점검

완료 기준:
- 품질 지표나 실패 사례를 포트폴리오에 기록할 수 있다.

### Phase 5 - Portfolio Wrap-up

목표:
- 결과물을 포트폴리오 형태로 정리한다.

작업:
- 최종 README 정리
- 데모 캡처 정리
- 시행착오와 개선 과정 정리
- 발표/면접용 설명 포인트 정리

완료 기준:
- 저장소만으로도 프로젝트의 가치와 진행 과정이 설명된다.

## 4. Priority Order

우선순위는 아래와 같다.

1. 텍스트 중심 PDF에서 동작하는 흐름
2. 근거 페이지가 보이는 질문응답
3. 요약 기능
4. OCR / 고도화
5. 배포와 포트폴리오 정리

## 5. Current Focus

지금 당장 해야 할 일:

- chunking 기준 정의
- retrieval 기준 메타데이터 구조 설계
- Vector Store 선택 기준 확정

### Next Commit Goal

다음 작업 단위는 아래 세 가지가 한 번에 보이게 만드는 것이다.

- chunk 데이터 구조 확정
- retrieval 실험 기준 정의
- Phase 2 시작점 문서화

### Phase 1 Task Checklist

- [x] 샘플 문서 후보 2~3개 수집
- [x] 최종 샘플 문서 1개 선택
- [x] Phase 1에서 사용할 저장 방식 확정
- [x] 업로드 API 입력/출력 형식 정의
- [x] 파싱 결과 데이터 구조 정의
- [x] 결과 확인 화면 또는 API 출력 형태 정의
- [x] Phase 1 완료 조건을 README / WORKLOG에 연결

### Phase 1 Follow-up Evidence

- [ ] 샘플 문서 기반 데모 캡처 또는 시연 기록 추가

### Recommended First Issue Breakdown

다음 구현은 아래 3개 이슈로 나누는 것을 권장한다.

1. `sample-doc-selection`
   - 공개 가능한 PDF 1개 선정
   - 선정 이유와 제외한 후보 기록

2. `phase1-api-contract`
   - 업로드 요청 형식
   - 파싱 응답 형식
   - 문서 메타데이터 형식

3. `phase1-vertical-slice`
   - 업로드
   - 페이지별 텍스트 추출
   - 결과 확인

### Locked Decisions For Phase 1

- 저장 방식: 로컬 PDF 파일 + 문서 id 기준 JSON 파싱 결과 저장
- 최소 API: `POST /documents/upload`, `GET /documents/{document_id}`
- 출력 단위: 업로드 직후에는 page summary, 상세 조회에서는 full page text

## 6. Sample Document Selection Rule

초기 샘플 문서는 아래 조건을 만족해야 한다.

- 공개 가능한 문서일 것
- 개인정보가 없을 것
- 텍스트 중심 PDF일 것
- 페이지 번호 확인이 가능할 것
- 질문 3~5개를 만들 수 있을 정도로 내용이 분명할 것

### Candidate Order

우선 후보는 아래 순서로 검토한다.

1. [NC DAC Sample Contract Template](https://www.dac.nc.gov/documents/files/sample-contract-template-0)
2. [Wells Fargo 2024 Annual Report](https://www.wellsfargo.com/about/investor-relations/annual-reports/)
3. [IDACORP Annual Reports](https://www.idacorpinc.com/investor-relations/financial-info/annual-reports/default.aspx)

## 7. Risks And Response

- 범위가 너무 커질 위험
  - 대응: OCR과 멀티모달 고도화는 후순위로 미룬다.

- 문서 품질 차이로 인해 데모가 불안정할 위험
  - 대응: 초기에 텍스트 중심 PDF만 사용한다.

- 구현은 했지만 포트폴리오 설명이 약해질 위험
  - 대응: 각 단계마다 WORKLOG를 업데이트한다.

## 8. Review Rule

각 Phase가 끝날 때마다 아래를 점검한다.

- 기능이 실제로 동작하는가
- README와 WORKLOG가 최신 상태인가
- 다음 단계가 명확한가
- 포트폴리오 관점에서 보여줄 메시지가 있는가
