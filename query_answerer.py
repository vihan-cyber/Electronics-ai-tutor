"""
Electronics AI Tutor - Query Answerer
Handles all LLM-based question answering with conversation memory.
"""
import logging

from knowledge_base import KnowledgeBase
from memory import ConversationMemory
from web_searcher import WebSearcher

logger = logging.getLogger(__name__)


class QueryAnswerer:

    @staticmethod
    def _build_prompt(question: str, context: str, memory: ConversationMemory, mode: str) -> str:
        history = memory.get_conversation_context()

        if mode == "local":
            history_block = f"\nPrevious Conversation:\n{history}\n" if history else ""
            return (
                f"You are an expert electronics tutor. Answer using ONLY the document excerpts below.\n"
                f"If the answer is not present, say \"I don't have that information in my documents.\"\n"
                f"Reference previous conversation where relevant.\n"
                f"{history_block}\n"
                f"Document Excerpts:\n{context}\n\n"
                f"Question: {question}\n\nStep-by-step answer:"
            )

        elif mode == "web":
            history_block = f"\nPrevious Conversation:\n{history}\n" if history else ""
            return (
                f"You are an expert electronics tutor. Answer using ONLY the web search results below.\n"
                f"If the answer is not present, say \"The web search did not provide enough information.\"\n"
                f"{history_block}\n"
                f"Web Search Results:\n{context}\n\n"
                f"Question: {question}\n\nStep-by-step answer (cite sources):"
            )

        return f"Question: {question}\n\nAnswer:"

    @staticmethod
    def answer_from_local_docs(question: str, memory: ConversationMemory, use_web_fallback: bool = False) -> str:
        kb = KnowledgeBase()
        if not kb.is_ready():
            return "⚠️ Knowledge base not ready. Please wait or click **Full Rebuild**."
        try:
            docs = kb.vectordb.similarity_search(question, k=kb.retrieval_k)
            if docs:
                context = "\n\n".join(
                    f"[Source: {d.metadata['source']}]\n{d.page_content}" for d in docs
                )
                prompt = QueryAnswerer._build_prompt(question, context, memory, "local")
                answer = kb.llm.invoke(prompt)
                sources = sorted(set(d.metadata["source"] for d in docs))
                citation = "\n\n---\n**📚 Sources:**\n" + "\n".join(f"- {s}" for s in sources)
                memory.add_turn("user", question)
                memory.add_turn("assistant", answer)
                return answer + citation

            if use_web_fallback:
                return QueryAnswerer.answer_from_web(question, memory)

            return "No relevant information found in your documents. Try enabling web fallback or clicking **Search Web**."
        except Exception as e:
            logger.error(f"Local answer error: {e}")
            return f"❌ Error: {e}"

    @staticmethod
    def answer_from_web(question: str, memory: ConversationMemory) -> str:
        kb = KnowledgeBase()
        if not kb.llm:
            return "⚠️ LLM not ready."
        if not WebSearcher.is_available():
            return "⚠️ Web search unavailable. Run: `pip install duckduckgo-search`"
        try:
            results = WebSearcher.search(question)
            if not results:
                return "No web results found. Check your internet connection."
            context = "\n\n".join(
                f"[{r['title']}]({r['url']})\n{r['snippet']}" for r in results
            )
            prompt = QueryAnswerer._build_prompt(question, context, memory, "web")
            answer = kb.llm.invoke(prompt)
            citation = "\n\n---\n**🌐 Web Sources:**\n" + "\n".join(
                f"- [{r['title']}]({r['url']})" for r in results
            )
            memory.add_turn("user", question)
            memory.add_turn("assistant", answer)
            return answer + citation
        except Exception as e:
            logger.error(f"Web answer error: {e}")
            return f"❌ Error: {e}"
