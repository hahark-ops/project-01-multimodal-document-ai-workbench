# Backend

이 디렉터리는 FastAPI 서버와 문서 파싱, 인덱싱, 질의응답 로직을 담습니다.

## Included

- FastAPI 앱 진입점
- health 체크 라우트
- PDF 업로드 및 문서 상세 조회 라우트
- 로컬 파일 저장
- PyMuPDF 기반 페이지별 텍스트 추출
- 기본 테스트 파일
- `uv` 기반 Python 프로젝트 설정

## Planned

- chunking / embedding / retrieval
- 요약 및 질문응답 로직

## Run

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```
