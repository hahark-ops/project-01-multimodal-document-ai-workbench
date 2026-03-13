import pytest


@pytest.fixture(autouse=True)
def phase1_storage(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("STORAGE_ROOT", str(tmp_path))
    yield
