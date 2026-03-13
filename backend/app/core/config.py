import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _resolve_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def get_frontend_origin() -> str:
    return os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")


def get_upload_dir() -> Path:
    return _resolve_path(os.getenv("UPLOAD_DIR", "data/uploads"))
