from pydantic import BaseModel, Field


class PageSummary(BaseModel):
    page_number: int
    char_count: int
    text_preview: str


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    page_count: int
    pages: list[PageSummary]


class PageDetail(BaseModel):
    page_number: int
    char_count: int
    text: str


class DocumentDetail(BaseModel):
    document_id: str
    filename: str
    status: str
    page_count: int
    pages: list[PageDetail]


class APIErrorDetail(BaseModel):
    code: str
    message: str


class APIErrorResponse(BaseModel):
    error: APIErrorDetail = Field(...)
