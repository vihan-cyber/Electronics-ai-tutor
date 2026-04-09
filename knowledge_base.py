"""
Electronics AI Tutor - Knowledge Base (Singleton)
"""
import logging
from typing import Optional

from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import Chroma

from config import Config
from models import ProcessResult

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Singleton: embeddings + vector DB + LLM"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.embeddings: Optional[OllamaEmbeddings] = None
        self.vectordb: Optional[Chroma] = None
        self.llm: Optional[OllamaLLM] = None
        self.current_model: str = Config.DEFAULT_MODEL
        self.retrieval_k: int = Config.RETRIEVAL_K
        self._initialized = True
        logger.info("KnowledgeBase singleton created")

    def init_embeddings(self) -> ProcessResult:
        try:
            if self.embeddings is None:
                self.embeddings = OllamaEmbeddings(model=Config.EMBEDDING_MODEL)
            return ProcessResult(True, "Embeddings ready")
        except Exception as e:
            return ProcessResult(False, f"❌ Embeddings failed: {e}")

    def init_llm(self, model_name: str) -> ProcessResult:
        try:
            if self.llm is None or self.current_model != model_name:
                self.llm = OllamaLLM(model=model_name, temperature=Config.TEMPERATURE)
                self.current_model = model_name
            return ProcessResult(True, f"✅ Model ready: {model_name}")
        except Exception as e:
            return ProcessResult(False, f"❌ LLM failed: {e}")

    def load_existing_db(self) -> ProcessResult:
        try:
            if not Config.VECTOR_DB_PATH.exists() or not any(Config.VECTOR_DB_PATH.iterdir()):
                return ProcessResult(False, "No existing database found")
            result = self.init_embeddings()
            if not result.success:
                return result
            self.vectordb = Chroma(
                persist_directory=str(Config.VECTOR_DB_PATH),
                embedding_function=self.embeddings
            )
            return ProcessResult(True, "Database loaded")
        except Exception as e:
            return ProcessResult(False, f"DB load failed: {e}")

    def is_ready(self) -> bool:
        return self.vectordb is not None and self.llm is not None

    def reset(self):
        self.embeddings = None
        self.vectordb = None
        self.llm = None
