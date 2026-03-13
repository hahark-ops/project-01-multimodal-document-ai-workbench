from datetime import datetime

from pydantic import BaseModel


class DocumentSummary(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime


class UploadResponse(BaseModel):
    document: DocumentSummary
    message: str
