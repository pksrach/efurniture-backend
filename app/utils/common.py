import os
from pathlib import Path

VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def is_valid_file_type(file_extension: str) -> bool:
    return file_extension.lower() in VALID_IMAGE_EXTENSIONS

def get_file_path(file_name: str) -> str:
    upload_dir = Path("uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    return str(upload_dir / file_name)