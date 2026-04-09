"""
Electronics AI Tutor - UI Callbacks
All Gradio event handlers. Memory is passed via gr.State.
"""
import shutil
import logging
from pathlib import Path
from typing import List

from config import Config
from knowledge_base import KnowledgeBase
from memory import ConversationMemory
from pdf_processor import KnowledgeBaseManager
from query_answerer import QueryAnswerer

logger = logging.getLogger(__name__)


class UICallbacks:

    @staticmethod
    def startup() -> str:
        Config.validate_and_create_dirs()
        kb = KnowledgeBase()
        result = kb.load_existing_db()
        if result.success:
            llm = kb.init_llm(Config.DEFAULT_MODEL)
            if llm.success:
                processed = KnowledgeBaseManager.load_processed_pdfs()
                return f"✅ Loaded existing DB — {len(processed)} PDF(s) indexed"
        result = KnowledgeBaseManager.rebuild_knowledge_base()
        return str(result)

    @staticmethod
    def chat_local(message: str, history: List, memory: ConversationMemory, use_web_fallback: bool):
        if not message.strip():
            return "", history
        response = QueryAnswerer.answer_from_local_docs(message, memory, use_web_fallback)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        return "", history

    @staticmethod
    def chat_web(message: str, history: List, memory: ConversationMemory):
        if not message.strip():
            return "", history
        response = QueryAnswerer.answer_from_web(message, memory)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        return "", history

    @staticmethod
    def upload_pdf(file) -> str:
        if not file:
            return "No file selected."
        try:
            dest = Config.DOCS_FOLDER / Path(file.name).name
            shutil.copy(file.name, dest)
            return str(KnowledgeBaseManager.add_pdf_incremental(dest))
        except Exception as e:
            return f"❌ Upload error: {e}"

    @staticmethod
    def update_model(model_name: str) -> str:
        if not model_name:
            return "⚠️ No model selected"
        return str(KnowledgeBase().init_llm(model_name))

    @staticmethod
    def update_k(k: int) -> str:
        k = int(k)
        KnowledgeBase().retrieval_k = k
        return f"✅ Retrieval set to {k} chunks"

    @staticmethod
    def rebuild_kb() -> str:
        return str(KnowledgeBaseManager.rebuild_knowledge_base())

    @staticmethod
    def toggle_memory(enabled: bool, memory: ConversationMemory) -> str:
        memory.toggle_enabled(enabled)
        return memory.get_summary()

    @staticmethod
    def update_memory_length(length: int, memory: ConversationMemory) -> str:
        memory.set_max_length(int(length))
        return memory.get_summary()

    @staticmethod
    def clear_memory(memory: ConversationMemory) -> str:
        memory.clear()
        return memory.get_summary()

    @staticmethod
    def clear_chat(memory: ConversationMemory):
        memory.clear()
        return [], memory.get_summary()
