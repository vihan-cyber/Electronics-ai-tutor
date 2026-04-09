"""
Electronics AI Tutor - PDF Processor & Knowledge Base Manager
"""
import os
import json
import time
import logging
from pathlib import Path
from typing import Dict

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from config import Config
from models import ProcessResult
from knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)


class PDFProcessor:
    @staticmethod
    def validate_file(file_path: Path) -> ProcessResult:
        if not file_path.exists():
            return ProcessResult(False, "File does not exist")
        size_mb = file_path.stat().st_size / (1024 * 1024)
        if size_mb > Config.MAX_PDF_SIZE_MB:
            return ProcessResult(False, f"⚠️ File too large ({size_mb:.1f} MB, max {Config.MAX_PDF_SIZE_MB} MB)")
        if file_path.suffix.lower() != '.pdf':
            return ProcessResult(False, "❌ Only PDF files are supported")
        return ProcessResult(True, "OK")

    @staticmethod
    def process_single_pdf(pdf_path: Path) -> ProcessResult:
        try:
            v = PDFProcessor.validate_file(pdf_path)
            if not v.success:
                return v
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=Config.CHUNK_SIZE,
                chunk_overlap=Config.CHUNK_OVERLAP
            )
            pages = PyMuPDFLoader(str(pdf_path)).load()
            chunks = [c for c in splitter.split_documents(pages) if c.page_content.strip()]
            for c in chunks:
                c.metadata["source"] = pdf_path.name
                c.metadata["processed_at"] = time.time()
            if not chunks:
                return ProcessResult(False, f"⚠️ No readable text in '{pdf_path.name}'")
            return ProcessResult(True, f"✅ {len(chunks)} chunks", chunks)
        except Exception as e:
            return ProcessResult(False, f"❌ PDF error: {e}")


class KnowledgeBaseManager:
    @staticmethod
    def load_processed_pdfs() -> Dict:
        if Config.PROCESSED_PDFS_JSON.exists():
            try:
                with open(Config.PROCESSED_PDFS_JSON) as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    @staticmethod
    def save_processed_pdfs(record: Dict) -> None:
        with open(Config.PROCESSED_PDFS_JSON, "w") as f:
            json.dump(record, f, indent=2)

    @staticmethod
    def add_pdf_incremental(pdf_path: Path) -> ProcessResult:
        kb = KnowledgeBase()
        try:
            result = kb.init_embeddings()
            if not result.success:
                return result
            if kb.vectordb is None:
                return KnowledgeBaseManager.rebuild_knowledge_base()
            processed = KnowledgeBaseManager.load_processed_pdfs()
            if pdf_path.name in processed:
                return ProcessResult(False, f"ℹ️ '{pdf_path.name}' already indexed")
            result = PDFProcessor.process_single_pdf(pdf_path)
            if not result.success:
                return result
            chunks = result.data
            ids = [f"{pdf_path.name}_{i}" for i in range(len(chunks))]
            kb.vectordb.add_documents(documents=chunks, ids=ids)
            processed[pdf_path.name] = {
                "last_modified": os.path.getmtime(pdf_path),
                "chunk_count": len(chunks),
                "chunk_ids": ids,
                "added_at": time.time()
            }
            KnowledgeBaseManager.save_processed_pdfs(processed)
            return ProcessResult(True, f"✅ Added '{pdf_path.name}' ({len(chunks)} chunks)")
        except Exception as e:
            return ProcessResult(False, f"❌ {e}")

    @staticmethod
    def rebuild_knowledge_base() -> ProcessResult:
        kb = KnowledgeBase()
        try:
            pdf_files = sorted([f for f in Config.DOCS_FOLDER.iterdir() if f.suffix.lower() == '.pdf'])
            if not pdf_files:
                return ProcessResult(False, "⚠️ No PDFs found in documents folder")
            result = kb.init_embeddings()
            if not result.success:
                return result
            all_chunks, metadata = [], {}
            for pdf in pdf_files:
                r = PDFProcessor.process_single_pdf(pdf)
                if r.success:
                    all_chunks.extend(r.data)
                    metadata[pdf.name] = {
                        "last_modified": os.path.getmtime(pdf),
                        "chunk_count": len(r.data),
                        "added_at": time.time()
                    }
                else:
                    logger.warning(f"Skipped {pdf.name}: {r.message}")
            if not all_chunks:
                return ProcessResult(False, "❌ No readable text in any PDFs")
            kb.vectordb = Chroma.from_documents(
                all_chunks, kb.embeddings,
                persist_directory=str(Config.VECTOR_DB_PATH)
            )
            result = kb.init_llm(Config.DEFAULT_MODEL)
            if not result.success:
                return result
            KnowledgeBaseManager.save_processed_pdfs(metadata)
            return ProcessResult(True, f"✅ Rebuilt: {len(all_chunks)} chunks from {len(pdf_files)} PDF(s)")
        except Exception as e:
            return ProcessResult(False, f"❌ Rebuild error: {e}")
