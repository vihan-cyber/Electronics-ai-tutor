"""
Electronics AI Tutor - Web Searcher
Single source of truth for web search. (web_search.py is no longer used)
"""
import logging
from typing import List, Dict

from config import Config

logger = logging.getLogger(__name__)

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    logger.warning("duckduckgo_search not installed. Run: pip install duckduckgo-search")


class WebSearcher:
    @staticmethod
    def is_available() -> bool:
        return DDGS_AVAILABLE

    @staticmethod
    def search(query: str, max_results: int = Config.WEB_SEARCH_MAX_RESULTS) -> List[Dict]:
        if not DDGS_AVAILABLE:
            return []
        for backend in ['html', 'api']:
            try:
                with DDGS(timeout=Config.WEB_SEARCH_TIMEOUT) as ddgs:
                    results = list(ddgs.text(query, max_results=max_results, backend=backend))
                    if results:
                        return [
                            {
                                "title": r.get("title", "No title"),
                                "snippet": r.get("body", r.get("description", "")),
                                "url": r.get("href", r.get("url", "#")),
                            }
                            for r in results
                        ]
            except Exception as e:
                logger.warning(f"Backend '{backend}' failed: {e}")
        return []
