from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class ChunkMetadata:
    chunk_id: str
    size: int
    created_at: datetime
    storage_location: str
    compression_type: str = "NONE"

@dataclass
class FileManifest:
    filename: str
    user_id: str
    chunk_hashes: List[str]
    total_size: int
    uploaded_at: datetime
    version: int = 1

@dataclass
class UploadResponse:
    success: bool
    message: str
    file_id: str
    chunks_processed: int
    chunks_stored: int
    total_size: int
