import fitz
from fastapi.testclient import TestClient

from app.api.routes import documents as document_routes
from app.main import app
from app.services.storage import StorageWriteError


def _build_test_pdf_bytes() -> bytes:
    document = fitz.open()
    page_1 = document.new_page()
    page_1.insert_textbox(
        fitz.Rect(72, 72, 520, 760),
        (
            "AGREEMENT. "
            "(1) CONTRACTUAL STATUS: The CONTRACTOR is not and will not by virtue of this "
            "contract acquire the status of an employee of the AGENCY. "
            "(2) TIME OF PERFORMANCE: The effective date of this agreement is January 1, 2026 "
            "and the termination date is December 31, 2026. "
            "(3) COMPENSATION: The AGENCY will pay the CONTRACTOR at an hourly rate for services performed. "
            "(5) INVOICE: Payment under this AGREEMENT will be made upon receipt of an original invoice."
        ),
        fontsize=11,
        lineheight=1.4,
    )
    page_2 = document.new_page()
    page_2.insert_textbox(
        fitz.Rect(72, 72, 520, 760),
        (
            "(7) FUNDING: This AGREEMENT shall automatically terminate if funds cease to be available. "
            "(9) TAXES: Failure to provide the AGENCY with a correct taxpayer number authorizes the "
            "AGENCY to withhold 20% of any amount due and payable under this AGREEMENT. "
            "(11) SITUS: This contract shall be governed by the laws of North Carolina. "
            "(15) ASSIGNMENT: The CONTRACTOR shall not subcontract any work without the written approval "
            "of the AGENCY."
        ),
        fontsize=11,
        lineheight=1.4,
    )
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
    assert upload_payload["chunk_count"] >= 2
    assert len(upload_payload["pages"]) == 2
    assert "contract" in upload_payload["pages"][0]["text_preview"].lower()
    assert (tmp_path / "uploads" / f"{upload_payload['document_id']}.pdf").exists()
    assert (tmp_path / "parsed" / f"{upload_payload['document_id']}.json").exists()
    assert (tmp_path / "chunks" / f"{upload_payload['document_id']}.json").exists()

    detail_response = client.get(f"/documents/{upload_payload['document_id']}")

    assert detail_response.status_code == 200
    detail_payload = detail_response.json()

    assert detail_payload["document_id"] == upload_payload["document_id"]
    assert detail_payload["chunk_count"] == upload_payload["chunk_count"]
    assert len(detail_payload["pages"]) == 2
    assert "north carolina" in detail_payload["pages"][1]["text"].lower()


def test_get_document_chunks_returns_chunk_metadata() -> None:
    client = TestClient(app)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("sample-contract-template.pdf", _build_test_pdf_bytes(), "application/pdf")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.get(f"/documents/{document_id}/chunks")

    assert response.status_code == 200
    payload = response.json()

    assert payload["document_id"] == document_id
    assert payload["chunk_count"] >= 2
    assert payload["chunks"][0]["page_number"] == 1
    assert "text_preview" in payload["chunks"][0]


def test_retrieval_search_returns_relevant_chunk() -> None:
    client = TestClient(app)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("sample-contract-template.pdf", _build_test_pdf_bytes(), "application/pdf")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        "/retrieval/search",
        json={"document_id": document_id, "query": "terminate notice", "top_k": 2},
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["document_id"] == document_id
    assert len(payload["results"]) == 2
    assert payload["results"][0]["page_number"] == 2
    assert "withhold 20%" in payload["results"][0]["text"].lower()


def test_grounded_answer_returns_answer_and_citations() -> None:
    client = TestClient(app)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("sample-contract-template.pdf", _build_test_pdf_bytes(), "application/pdf")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        "/answers/ask",
        json={
            "document_id": document_id,
            "question": "taxpayer number withhold 20%",
            "top_k": 3,
            "max_citations": 2,
        },
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["document_id"] == document_id
    assert payload["answer_strategy"] == "extractive-grounded-baseline"
    assert payload["answer_text"]
    assert len(payload["citations"]) >= 1
    assert payload["citations"][0]["page_number"] == 2
    assert "withhold 20%" in payload["citations"][0]["excerpt"].lower()


def test_grounded_answer_missing_chunks_returns_not_found() -> None:
    client = TestClient(app)

    response = client.post(
        "/answers/ask",
        json={
            "document_id": "doc_missing",
            "question": "taxpayer number",
        },
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "DOCUMENT_CHUNKS_NOT_FOUND"


def test_summary_generation_returns_key_points() -> None:
    client = TestClient(app)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("sample-contract-template.pdf", _build_test_pdf_bytes(), "application/pdf")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        "/summaries/generate",
        json={"document_id": document_id, "max_points": 3, "max_highlights": 3},
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["document_id"] == document_id
    assert payload["summary_strategy"] == "extractive-summary-baseline"
    assert len(payload["key_points"]) == 3
    assert len(payload["highlights"]) == 3
    assert "contractual status" in payload["summary_text"].lower()


def test_evaluation_run_returns_metrics_and_cases() -> None:
    client = TestClient(app)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("sample-contract-template.pdf", _build_test_pdf_bytes(), "application/pdf")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        "/evaluations/run",
        json={
            "document_id": document_id,
            "suite_id": "nc_dac_sample_contract_v1",
            "top_k": 3,
            "max_citations": 2,
        },
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["document_id"] == document_id
    assert payload["suite_id"] == "nc_dac_sample_contract_v1"
    assert payload["metrics"]["question_count"] == 5
    assert len(payload["cases"]) == 5
    assert payload["metrics"]["retrieval_hit_rate"] >= 0.8


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
