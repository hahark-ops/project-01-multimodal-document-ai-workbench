# Backend

이 디렉터리는 FastAPI 서버와 문서 파싱, 인덱싱, 질의응답 로직을 담습니다.

## Included

- FastAPI 앱 진입점
- health 체크 라우트
- 문서 업로드용 placeholder 라우트
- 기본 테스트 파일
- `uv` 기반 Python 프로젝트 설정

## Planned

- PDF 저장 및 파싱
- chunking / embedding / retrieval
- 요약 및 질문응답 로직

## Run

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```
