import re
from pathlib import Path

from app.schemas.documents import PageDetail


class PDFParseError(Exception):
    """Raised when a PDF cannot be parsed."""


def _normalize_text(text: str) -> str:
    collapsed = re.sub(r"\n{3,}", "\n\n", text)
    return collapsed.strip()


def parse_pdf(file_path: Path) -> list[PageDetail]:
    try:
        import fitz
    except ImportError as exc:  # pragma: no cover
        raise PDFParseError("PyMuPDF is not installed.") from exc

    try:
        parsed_pages: list[PageDetail] = []
        with fitz.open(file_path) as document:
            for index, page in enumerate(document, start=1):
                page_text = _normalize_text(page.get_text("text"))
                parsed_pages.append(
                    PageDetail(
                        page_number=index,
                        char_count=len(page_text),
                        text=page_text,
                    )
                )
        return parsed_pages
    except Exception as exc:
        raise PDFParseError(f"Failed to parse PDF: {exc}") from exc
