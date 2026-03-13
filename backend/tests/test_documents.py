import fitz
from fastapi.testclient import TestClient

from app.main import app


def _build_test_pdf_bytes() -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Hello from test PDF")
    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


def test_health_check() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_pdf_and_fetch_document_detail(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))
    client = TestClient(app)

    response = client.post(
        "/documents/upload",
        files={"file": ("sample.pdf", _build_test_pdf_bytes(), "application/pdf")},
    )

    assert response.status_code == 201
    payload = response.json()

    assert payload["message"] == "File uploaded and parsed successfully."
    assert payload["document"]["filename"] == "sample.pdf"
    assert payload["document"]["status"] == "parsed"
    assert payload["document"]["page_count"] == 1
    assert payload["document"]["extracted_char_count"] > 0
    assert "Hello from test PDF" in payload["document"]["pages"][0]["text"]
    assert len(list(tmp_path.iterdir())) == 1

    document_id = payload["document"]["id"]
    detail_response = client.get(f"/documents/{document_id}")

    assert detail_response.status_code == 200
    assert detail_response.json()["id"] == document_id


def test_reject_non_pdf_upload() -> None:
    client = TestClient(app)

    response = client.post(
        "/documents/upload",
        files={"file": ("notes.txt", b"plain text", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF uploads are supported in the current MVP."
