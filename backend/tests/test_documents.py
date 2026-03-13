import fitz
from fastapi.testclient import TestClient

from app.api.routes import documents as document_routes
from app.main import app
from app.services.storage import StorageWriteError


def _build_test_pdf_bytes() -> bytes:
    document = fitz.open()
    page_1 = document.new_page()
    page_1.insert_text((72, 72), "This contract is entered into by both parties.")
    page_2 = document.new_page()
    page_2.insert_text((72, 72), "Either party may terminate with written notice.")
    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


def test_health_check() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_pdf_and_fetch_document_detail(tmp_path) -> None:
    client = TestClient(app)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("sample-contract-template.pdf", _build_test_pdf_bytes(), "application/pdf")},
    )

    assert upload_response.status_code == 201
    upload_payload = upload_response.json()

    assert upload_payload["status"] == "parsed"
    assert upload_payload["filename"] == "sample-contract-template.pdf"
    assert upload_payload["page_count"] == 2
    assert len(upload_payload["pages"]) == 2
    assert "contract" in upload_payload["pages"][0]["text_preview"].lower()
    assert (tmp_path / "uploads" / f"{upload_payload['document_id']}.pdf").exists()
    assert (tmp_path / "parsed" / f"{upload_payload['document_id']}.json").exists()

    detail_response = client.get(f"/documents/{upload_payload['document_id']}")

    assert detail_response.status_code == 200
    detail_payload = detail_response.json()

    assert detail_payload["document_id"] == upload_payload["document_id"]
    assert len(detail_payload["pages"]) == 2
    assert "written notice" in detail_payload["pages"][1]["text"].lower()


def test_reject_non_pdf_upload() -> None:
    client = TestClient(app)

    response = client.post(
        "/documents/upload",
        files={"file": ("notes.txt", b"plain text", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "UNSUPPORTED_FILE_TYPE"


def test_reject_empty_pdf_upload() -> None:
    client = TestClient(app)

    response = client.post(
        "/documents/upload",
        files={"file": ("empty.pdf", b"", "application/pdf")},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "EMPTY_FILE"


def test_missing_document_returns_not_found_error_shape() -> None:
    client = TestClient(app)

    response = client.get("/documents/doc_missing")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "DOCUMENT_NOT_FOUND"


def test_upload_storage_failure_keeps_documented_error_shape(monkeypatch) -> None:
    client = TestClient(app)

    async def failing_save_upload_stream(document_id: str, upload) -> tuple[object, int]:
        raise StorageWriteError("Uploaded file could not be saved.")

    monkeypatch.setattr(document_routes, "save_upload_stream", failing_save_upload_stream)

    response = client.post(
        "/documents/upload",
        files={"file": ("sample-contract-template.pdf", _build_test_pdf_bytes(), "application/pdf")},
    )

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "FILE_SAVE_FAILED"


def test_corrupted_parsed_document_returns_structured_error(tmp_path) -> None:
    client = TestClient(app)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("sample-contract-template.pdf", _build_test_pdf_bytes(), "application/pdf")},
    )
    document_id = upload_response.json()["document_id"]

    parsed_file = tmp_path / "parsed" / f"{document_id}.json"
    parsed_file.write_text("{invalid json", encoding="utf-8")

    response = client.get(f"/documents/{document_id}")

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "PARSED_DOCUMENT_LOAD_FAILED"


def test_validation_error_keeps_documented_error_shape() -> None:
    client = TestClient(app)

    response = client.post("/documents/upload")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
