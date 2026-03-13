from app.schemas.documents import DocumentDetail, DocumentSummary

_documents: dict[str, DocumentDetail] = {}


def list_document_summaries() -> list[DocumentSummary]:
    return [
        DocumentSummary(
            id=document.id,
            filename=document.filename,
            status=document.status,
            created_at=document.created_at,
            page_count=document.page_count,
            extracted_char_count=document.extracted_char_count,
        )
        for document in _documents.values()
    ]


def get_document(document_id: str) -> DocumentDetail | None:
    return _documents.get(document_id)


def save_document(document: DocumentDetail) -> None:
    _documents[document.id] = document


def clear_documents() -> None:
    _documents.clear()
