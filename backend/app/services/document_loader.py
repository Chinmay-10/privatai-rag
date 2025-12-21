from pathlib import Path
from typing import List, Tuple, Dict
import hashlib
import uuid

import fitz  

from app.core.config import settings

def get_tenant_storage(tenant_id: str) -> Path:
    """
    Returns tenant-isolated storage directory.
    Designed to be mounted as a Docker volume.
    """
    base = Path(settings.FILE_STORE)
    tenant_dir = base / tenant_id
    tenant_dir.mkdir(parents=True, exist_ok=True)
    return tenant_dir

def compute_sha256(path: Path) -> str:
    """
    Compute SHA256 hash of file for integrity + deduplication.
    """
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def extract_text_from_pdf(path: Path) -> str:
    """
    Deterministic PDF text extraction.
    """
    doc = fitz.open(path)
    pages = []

    for page in doc:
        pages.append(page.get_text("text"))

    return "\n".join(pages).strip()


def chunk_text(
    text: str,
    chunk_size: int = 400,
    overlap: int = 80,
) -> List[str]:
    """
    Overlapping chunking with conservative defaults
    to reduce context bleed across sections.
    """
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def load_and_chunk(
    file,
    tenant_id: str,
) -> Tuple[List[str], Dict]:
    """
    Authoritative document ingestion pipeline.

    Guarantees:
    - Stable document ID
    - Content hash
    - Tenant isolation
    - Traceable metadata
    """

    tenant_dir = get_tenant_storage(tenant_id)

    document_id = str(uuid.uuid4())
    filename = file.filename

    stored_path = tenant_dir / f"{document_id}_{filename}"

    # Save file
    with open(stored_path, "wb") as f:
        f.write(file.file.read())

    # Compute integrity hash
    content_hash = compute_sha256(stored_path)

    # Extract & chunk
    text = extract_text_from_pdf(stored_path)
    chunks = chunk_text(text)

    metadata = {
        "document_id": document_id,
        "doc_name": filename,
        "tenant_id": tenant_id,
        "content_hash": content_hash,
        "file_path": str(stored_path),
        "chunk_count": len(chunks),
    }

    return chunks, metadata

from pathlib import Path
from app.core.config import settings


def list_documents(tenant_id: str):
    """
    List document names for a given tenant.
    Reads from tenant-isolated storage directory.
    """
    tenant_dir = Path(settings.FILE_STORE) / tenant_id

    if not tenant_dir.exists():
        return []

    return [
        f.name.split("_", 1)[1]  # remove UUID prefix
        for f in tenant_dir.iterdir()
        if f.is_file()
    ]
