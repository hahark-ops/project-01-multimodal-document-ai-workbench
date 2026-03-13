import json
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from pydantic import ValidationError

from app.core.config import get_parsed_dir, get_uploads_dir
from app.schemas.documents import DocumentDetail


class StorageWriteError(Exception):
    pass


class ParsedDocumentLoadError(Exception):
    pass


def ensure_storage_dirs() -> None:
    get_uploads_dir().mkdir(parents=True, exist_ok=True)
    get_parsed_dir().mkdir(parents=True, exist_ok=True)


def create_document_id() -> str:
    return f"doc_{uuid4().hex[:12]}"


async def save_upload_stream(document_id: str, upload: UploadFile) -> tuple[Path, int]:
    ensure_storage_dirs()
    file_path = get_uploads_dir() / f"{document_id}.pdf"
    total_bytes = 0

    try:
        with file_path.open("wb") as file_handle:
            while True:
                chunk = await upload.read(1024 * 1024)
                if not chunk:
                    break
                total_bytes += len(chunk)
                file_handle.write(chunk)
    except OSError as exc:
        file_path.unlink(missing_ok=True)
        raise StorageWriteError("Uploaded file could not be saved.") from exc

    return file_path, total_bytes


def save_parsed_document(document: DocumentDetail) -> Path:
    ensure_storage_dirs()
    file_path = get_parsed_dir() / f"{document.document_id}.json"
    temp_path = file_path.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps(document.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_path.replace(file_path)
    return file_path


def load_parsed_document(document_id: str) -> DocumentDetail | None:
    file_path = get_parsed_dir() / f"{document_id}.json"
    if not file_path.exists():
        return None
    try:
        return DocumentDetail.model_validate_json(file_path.read_text(encoding="utf-8"))
    except (OSError, ValidationError, ValueError) as exc:
        raise ParsedDocumentLoadError("Stored parsed document is unreadable.") from exc
