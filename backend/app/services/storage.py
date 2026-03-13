import json
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from pydantic import ValidationError

from app.core.config import get_chunks_dir, get_parsed_dir, get_uploads_dir
from app.schemas.documents import DocumentDetail
from app.schemas.retrieval import StoredChunk


class StorageWriteError(Exception):
    pass


class ParsedDocumentLoadError(Exception):
    pass


def ensure_storage_dirs() -> None:
    get_uploads_dir().mkdir(parents=True, exist_ok=True)
    get_parsed_dir().mkdir(parents=True, exist_ok=True)
    get_chunks_dir().mkdir(parents=True, exist_ok=True)


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


def save_document_chunks(document_id: str, chunks: list[StoredChunk]) -> Path:
    ensure_storage_dirs()
    file_path = get_chunks_dir() / f"{document_id}.json"
    temp_path = file_path.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps([chunk.model_dump() for chunk in chunks], ensure_ascii=False, indent=2),
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


def load_document_chunks(document_id: str) -> list[StoredChunk] | None:
    file_path = get_chunks_dir() / f"{document_id}.json"
    if not file_path.exists():
        return None
    try:
        raw_chunks = json.loads(file_path.read_text(encoding="utf-8"))
        return [StoredChunk.model_validate(item) for item in raw_chunks]
    except (OSError, ValidationError, ValueError, TypeError) as exc:
        raise ParsedDocumentLoadError("Stored document chunks are unreadable.") from exc


def load_all_document_chunks() -> list[StoredChunk]:
    ensure_storage_dirs()
    chunks: list[StoredChunk] = []
    for file_path in sorted(get_chunks_dir().glob("*.json")):
        document_id = file_path.stem
        loaded = load_document_chunks(document_id)
        if loaded:
            chunks.extend(loaded)
    return chunks


def delete_document_assets(document_id: str) -> None:
    paths = [
        get_uploads_dir() / f"{document_id}.pdf",
        get_parsed_dir() / f"{document_id}.json",
        get_chunks_dir() / f"{document_id}.json",
    ]
    for path in paths:
        path.unlink(missing_ok=True)
