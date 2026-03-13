# Multimodal Document AI Workbench

텍스트, 표, 이미지가 섞인 PDF 문서를 업로드하면 내용을 파싱하고, 근거 기반 질문응답과 요약을 제공하는 포트폴리오 프로젝트입니다.

## Current Status

- 상태: 재시작 완료, 문서 중심 계획 단계
- 시작일: 2026-03-13
- 대상: AWS AI School 포트폴리오 프로젝트
- 현재 저장소 구성: 계획 문서 4개만 유지

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

- 텍스트 중심 PDF 1개 이상 업로드
- 페이지별 텍스트 추출
- 파싱 결과 화면 표시

이 첫 단계를 통과한 뒤 retrieval, grounded answer, 요약 기능을 순서대로 붙입니다.

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

초기 데모는 아래 문서 유형을 상정합니다.

- 공개 취업공고 PDF
- 개인정보가 제거된 계약서 템플릿
- 직접 작성한 보고서 형식 PDF
