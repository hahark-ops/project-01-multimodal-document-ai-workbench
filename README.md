# Multimodal Document AI Workbench

계약서, 취업공고, 사내 문서처럼 텍스트와 표, 이미지가 섞인 문서를 업로드하면 내용을 파싱하고, 근거와 함께 질문응답 및 요약을 제공하는 멀티모달 문서 AI 프로젝트입니다.

## Project Status

- 현재 단계: 첫 vertical slice 구현 완료
- 시작일: 2026-03-13
- 목적: AWS AI School 포트폴리오 프로젝트
- 진행 기록: [docs/WORKLOG.md](docs/WORKLOG.md)
- 아키텍처 문서: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 현재 구현 범위: PDF 업로드, 로컬 저장, 페이지별 텍스트 추출, 업로드 결과 UI 표시

## Why This Project

실무 문서는 텍스트만 있는 경우보다 표, 차트, 스캔 이미지가 함께 포함된 경우가 많습니다. 단순 챗봇만으로는 이런 문서에 대해 신뢰도 높은 답변을 만들기 어렵고, 특히 "어디를 근거로 답했는지"를 설명하지 못하면 실제 업무에서 활용하기 어렵습니다.

이 프로젝트는 문서 파싱, 검색, 재정렬, 답변 생성, 출처 표기, 평가까지 이어지는 RAG 파이프라인을 직접 설계하고 구현해 보는 것을 목표로 합니다.

## Project Goal

- PDF, 이미지, 스캔 문서를 업로드할 수 있다.
- 문서에서 텍스트와 표, 이미지 설명을 추출하고 저장한다.
- 사용자 질문에 대해 근거 문단과 페이지 번호를 함께 제시한다.
- 문서 요약과 핵심 항목 추출 기능을 제공한다.
- 평가셋으로 retrieval 성능과 grounded answer 품질을 점검한다.

## MVP Scope

- 문서 업로드 UI 또는 간단한 대시보드
- OCR 및 문서 파싱 파이프라인
- chunking 및 멀티모달 인덱싱
- 문서 질문응답 RAG
- 답변 근거 문단 및 페이지 표시
- 문서 요약 및 핵심 정보 추출
- 기본 평가셋과 결과 기록

## Selected Initial Stack

구현 난도와 포트폴리오 완성 가능성을 같이 고려해 아래 조합으로 시작합니다.

- Frontend: Next.js, Tailwind CSS
- Backend: FastAPI
- Parsing: PyMuPDF
- OCR: Tesseract
- Embedding / LLM: provider abstraction을 두고 OpenAI 또는 Bedrock 연결
- Vector DB: Qdrant
- Storage: local file storage로 시작하고 이후 S3 확장
- Infra: Docker Compose 기반 로컬 개발, 이후 AWS 배포 확장

선정 이유는 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)에 정리했습니다.

## Repository Structure

```text
.
├── backend/        # FastAPI 서버와 파싱/RAG 파이프라인
├── data/           # 샘플 문서 및 로컬 데이터 가이드
├── docs/           # 아키텍처, 작업 기록, 설계 문서
├── frontend/       # Next.js 사용자 인터페이스
├── infra/          # Docker/AWS 배포 관련 설정
└── scripts/        # 개발 보조 스크립트
```

## Milestones

- [x] 프로젝트 아이디어 정리 및 README 초안 작성
- [x] GitHub 저장소 생성 및 초기 커밋
- [x] 포트폴리오형 README 구조 재정리
- [x] 최종 아키텍처 및 폴더 구조 결정
- [x] 프론트엔드/백엔드 기본 프로젝트 생성
- [x] 첫 vertical slice 구현
- [ ] 문서 업로드 및 파싱 파이프라인 고도화
- [ ] chunking 및 인덱싱 파이프라인 구축
- [ ] 근거 기반 문서 질의응답 구현
- [ ] 문서 요약 및 핵심 항목 추출 구현
- [ ] 평가셋 구축 및 성능 측정
- [ ] 배포 및 최종 포트폴리오 정리

## What To Show In Portfolio

- 왜 파인튜닝보다 먼저 RAG를 선택했는지
- 문서 파싱, chunking, reranking이 정확도에 어떤 영향을 줬는지
- hallucination을 줄이기 위해 출처 표기와 평가셋을 어떻게 설계했는지
- latency와 비용을 어떤 기준으로 관리했는지
- 문서 유형별 실패 사례와 개선 과정을 어떻게 기록했는지

## Success Metrics

- top-k retrieval accuracy
- grounded answer rate
- answer latency
- 문서 유형별 실패 사례와 개선 전후 비교

## Repository Rules

- 의미 있는 작업 단위로 커밋한다.
- 큰 단계가 끝날 때마다 README와 작업 기록 문서를 업데이트한다.
- API 키, 민감한 문서, 개인정보는 저장소에 올리지 않는다.
- 구현 전 단계에서도 계획과 판단 근거를 문서로 남긴다.

## Next Step

- 파싱 결과를 chunk 단위 데이터로 변환
- 임베딩 생성 및 Qdrant 저장 연결
- 문서 상세 화면에서 파싱 결과와 이후 검색 결과를 함께 보여주기
- 샘플 문서 2~3종 확보 및 평가 기준 초안 작성
