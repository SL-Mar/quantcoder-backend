import os
from fastapi import UploadFile
from backend.core.config import settings

# Base directory where all files are stored
USER_WORKDIR = settings.USER_WORKDIR

def ensure_folder_exists(folder_path: str):
    os.makedirs(folder_path, exist_ok=True)

async def save_uploaded_file(file: UploadFile, folder_path: str) -> str:
    """
    Save an uploaded file to the specified folder and return its full path.
    """
    ensure_folder_exists(folder_path)
    path = os.path.join(folder_path, file.filename)
    contents = await file.read()
    with open(path, "wb") as f:
        f.write(contents)
    return path

def save_file(path: str, content: str):
    """
    Write text content to a file, creating any necessary directories.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def delete_file(path: str):
    """
    Delete a file from disk if it exists.
    """
    if os.path.exists(path):
        os.remove(path)

def list_summaries(folder_path: str) -> list[str]:
    """
    List all .txt files in the specified folder.
    """
    if not os.path.exists(folder_path):
        return []
    return [
        fname for fname in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, fname)) and fname.endswith('.txt')
    ]
