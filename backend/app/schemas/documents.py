from datetime import datetime

from pydantic import BaseModel


class DocumentPage(BaseModel):
    page_number: int
    text: str
    char_count: int


class DocumentSummary(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime
    page_count: int
    extracted_char_count: int


class DocumentDetail(DocumentSummary):
    pages: list[DocumentPage]


class UploadResponse(BaseModel):
    document: DocumentDetail
    message: str
