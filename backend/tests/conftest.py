import pytest

from app.repositories.documents import clear_documents


@pytest.fixture(autouse=True)
def reset_document_store() -> None:
    clear_documents()
    yield
    clear_documents()
