# Multimodal Document AI Workbench

텍스트, 표, 이미지가 섞인 PDF 문서를 업로드하면 내용을 파싱하고, 근거 기반 질문응답과 요약을 제공하는 포트폴리오 프로젝트입니다.

## Current Status

- 상태: Phase 2 retrieval foundation 구현 완료, 샘플 문서 데모 기록 보강 예정
- 시작일: 2026-03-13
- 대상: AWS AI School 포트폴리오 프로젝트
- 현재 저장소 구성: 계획 문서 + Phase 2 코드 구현

## Document Map

- 프로젝트 개요와 기준점: [README.md](README.md)
- 기술 방향과 시스템 설계: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 실제 진행 기록: [docs/WORKLOG.md](docs/WORKLOG.md)
- 단계별 실행 계획: [docs/PLAN.md](docs/PLAN.md)

## Why This Project

실무 문서는 텍스트만 있는 것이 아니라 표, 차트, 스캔 이미지가 함께 포함되는 경우가 많습니다. 이런 문서에서는 단순 챗봇보다, "어떤 근거를 바탕으로 답했는지"를 보여주는 시스템이 더 중요합니다.

이 프로젝트는 문서 파싱, 검색, 근거 제시, 요약, 평가까지 이어지는 멀티모달 문서 AI 시스템을 직접 설계하고 구현하는 것을 목표로 합니다.

## MVP Goal

최종 MVP 기준으로 아래 기능을 목표로 합니다.

- PDF 문서를 업로드할 수 있다.
- 페이지 단위 텍스트를 추출하고 저장할 수 있다.
- 문서 질문에 대해 관련 문단과 페이지 번호를 함께 제시할 수 있다.
- 문서 전체 요약과 핵심 정보 추출 결과를 보여줄 수 있다.
- 최소한의 평가 질문 세트로 retrieval 품질을 점검할 수 있다.

## First Vertical Slice

가장 먼저 만들 기능은 최종 MVP 전체가 아니라 아래 범위입니다.

- [x] 텍스트 중심 PDF 1개 이상 업로드
- [x] 페이지별 텍스트 추출
- [x] 파싱 결과 화면 표시

이 첫 단계를 통과한 뒤 retrieval, grounded answer, 요약 기능을 순서대로 붙입니다.

현재 구현된 범위:

- FastAPI 기반 `POST /documents/upload`
- FastAPI 기반 `GET /documents/{document_id}`
- 로컬 PDF 저장
- JSON 기반 파싱 결과 저장
- Next.js 업로드 UI와 페이지별 텍스트 결과 화면

## Current Retrieval Foundation

Phase 2에서 추가로 구현한 범위는 아래와 같습니다.

- 문서별 chunk 생성과 JSON 저장
- `GET /documents/{document_id}/chunks`
- `POST /retrieval/search`
- top-k retrieval 결과 반환
- Next.js retrieval playground UI
- 문서별 chunk preview와 검색 결과 확인

현재 저장소에 남아 있는 검증 근거:

- 자동화 테스트로 PDF 업로드, 상세 조회, chunk 조회, retrieval 검색, 파일 검증, 에러 응답 형식 확인
- 프론트엔드 프로덕션 빌드 통과
- 샘플 문서를 사용한 실제 데모 캡처와 회고는 이후 포트폴리오 정리 단계에서 추가

## Repository Principle

- 구현 전에 문서로 방향을 먼저 정리한다.
- 한 번에 큰 기능을 만들지 않고 작은 vertical slice부터 만든다.
- 각 단계는 GitHub 커밋과 작업 기록으로 남긴다.
- 민감한 문서, 개인정보, API 키는 저장소에 올리지 않는다.

## What This Repository Should Show

- 문제를 어떻게 정의했는지
- 왜 그 기술 선택을 했는지
- 어떤 순서로 구현 범위를 줄였는지
- 정확도와 신뢰도를 어떻게 검증했는지
- 시행착오를 어떻게 기록하고 개선했는지

## Portfolio Signals

이 프로젝트로 보여주고 싶은 역량은 아래와 같습니다.

- 문서 AI 문제 정의와 범위 조절 능력
- RAG 파이프라인 설계 능력
- 근거 기반 응답과 평가 기준 설계 능력
- AWS 확장을 고려한 현실적인 기술 선택 능력
- GitHub 기록과 회고를 통한 문제 해결 과정 정리 능력

## Demo Scenario Candidates

Phase 1에 사용할 첫 기준 문서는 아래와 같습니다.

- 선택 문서: [NC DAC Sample Contract Template](https://www.dac.nc.gov/documents/files/sample-contract-template-0)
- 선택 이유:
  - 공개 가능한 공식 PDF
  - 텍스트 중심 문서
  - 2페이지 분량이라 첫 vertical slice에 적합
  - 계약 문서 구조가 분명해서 이후 질문응답 예시를 만들기 쉽다.

백업 후보:

- [Wells Fargo 2024 Annual Report](https://www.wellsfargo.com/about/investor-relations/annual-reports/)
- [IDACORP Annual Reports](https://www.idacorpinc.com/investor-relations/financial-info/annual-reports/default.aspx)

## Verification

- backend: `uv run pytest` 통과
- frontend: `npm run build` 통과
