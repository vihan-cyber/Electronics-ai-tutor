"""
Electronics AI Tutor - Configuration
"""
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class Config:
    """Centralized configuration management"""
    BASE_DIR = Path.cwd()
    DOCS_FOLDER = BASE_DIR / "electronics_docs"
    VECTOR_DB_PATH = BASE_DIR / "chroma_db"
    PROCESSED_PDFS_JSON = BASE_DIR / "processed_pdfs.json"
    FAVICON_PATH = BASE_DIR / "favicon.ico"

    DEFAULT_MODEL = "llama3.2:3b"
    EMBEDDING_MODEL = "nomic-embed-text"
    TEMPERATURE = 0.2

    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    RETRIEVAL_K = 5
    MAX_PDF_SIZE_MB = 200

    WEB_SEARCH_TIMEOUT = 10
    WEB_SEARCH_MAX_RESULTS = 3

    DEFAULT_MEMORY_ENABLED = True
    DEFAULT_MEMORY_LENGTH = 5
    MAX_MEMORY_LENGTH = 20

    @classmethod
    def validate_and_create_dirs(cls):
        cls.DOCS_FOLDER.mkdir(exist_ok=True)
        cls.VECTOR_DB_PATH.mkdir(exist_ok=True)
