# Multimodal Document AI Workbench

## Summary

계약서, 취업공고, 사내 문서, 표와 차트가 포함된 PDF/이미지를 업로드하면 내용을 파싱하고, 근거를 붙여 질의응답과 요약을 제공하는 멀티모달 문서 AI 워크벤치.

## MVP

- PDF, 이미지, 스캔 문서 업로드
- OCR 또는 문서 파싱 파이프라인 구축
- 텍스트, 표, 이미지 설명을 함께 저장하는 멀티모달 인덱싱
- 문서 질문응답 RAG
- 답변에 근거 문단과 페이지 번호 표시
- 문서 요약과 핵심 항목 추출
- 기본 평가셋으로 retrieval hit rate, answer quality 점검
- 간단한 웹 UI 또는 대시보드 제공

## Difficulty

- 전체 난이도: 중상
- 어려운 이유:
  - 문서 파싱 결과 품질이 일정하지 않다.
  - 표, 차트, 스캔 문서가 섞이면 파이프라인이 복잡해진다.
  - "답을 잘 말하는 것"보다 "근거를 정확히 찾는 것"이 더 어렵다.
- 일정 관리 포인트:
  - 첫 단계는 텍스트 중심 문서부터 시작
  - 이후 표/이미지 이해를 붙이는 방식으로 확장

## Tech Stack

- Frontend: Next.js or React, Tailwind CSS
- Backend: FastAPI or NestJS
- AI orchestration: LangChain or LlamaIndex
- Parsing/OCR: PyMuPDF, Unstructured, Tesseract, PaddleOCR
- Embedding: Amazon Nova Multimodal Embeddings or open-source multilingual embeddings
- Vector DB: OpenSearch, pgvector, or Qdrant
- Reranking: cross-encoder reranker or Bedrock reranking stack
- LLM/VLM: Amazon Bedrock models, OpenAI responses models, or open-source VLM
- Storage: S3
- Infra: Docker, ECS/EKS or EC2, CloudWatch/Grafana
- Evaluation: RAGAS, custom eval set, latency/cost logging

## Portfolio Positioning

- 한 줄 소개:
  - "멀티모달 문서를 대상으로 근거 기반 검색과 요약을 제공하는 문서 AI 시스템을 구축했다."
- 문제 정의:
  - 실무 문서는 텍스트만 있는 게 아니라 표, 차트, 스캔 이미지가 섞여 있어 단순 챗봇으로는 신뢰도 높은 답변이 어렵다.
- 면접에서 강조할 것:
  - 왜 파인튜닝보다 먼저 RAG를 선택했는지
  - chunking, parsing, reranking이 정확도에 미친 영향
  - hallucination을 줄이기 위해 출처 표기와 평가셋을 어떻게 설계했는지
  - latency와 비용을 어떻게 관리했는지
- 보여주면 좋은 지표:
  - top-k retrieval accuracy
  - grounded answer rate
  - answer latency
  - 문서 유형별 실패 사례와 개선 전후 비교

## Nice-to-Have

- 문서 비교 기능
- structured JSON extraction
- 팀 협업용 문서 컬렉션 관리
- human feedback 기반 answer quality 개선
