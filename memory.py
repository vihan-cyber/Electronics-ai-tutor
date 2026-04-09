"""
Electronics AI Tutor - Conversation Memory
"""
import time
import logging
from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Any

from config import Config

logger = logging.getLogger(__name__)


@dataclass
class ConversationTurn:
    role: str
    content: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {"role": self.role, "content": self.content, "timestamp": self.timestamp}


class ConversationMemory:
    """Manages conversation history with configurable memory length"""

    def __init__(self, max_length: int = Config.DEFAULT_MEMORY_LENGTH):
        self.memory: deque = deque(maxlen=max_length)
        self.max_length = max_length
        self.enabled = Config.DEFAULT_MEMORY_ENABLED
        logger.info(f"ConversationMemory initialized (max_length={max_length})")

    def add_turn(self, role: str, content: str) -> None:
        if not self.enabled:
            return
        self.memory.append(ConversationTurn(role=role, content=content))

    def get_conversation_context(self, max_chars: int = 2000) -> str:
        if not self.memory or not self.enabled:
            return ""
        lines = [f"{t.role.capitalize()}: {t.content}" for t in self.memory]
        history = "\n".join(lines)
        if len(history) > max_chars:
            history = "..." + history[-max_chars:]
        return history

    def set_max_length(self, max_length: int) -> None:
        if max_length < 1:
            return
        self.memory = deque(list(self.memory), maxlen=max_length)
        self.max_length = max_length

    def toggle_enabled(self, enabled: bool) -> None:
        self.enabled = enabled

    def clear(self) -> None:
        self.memory.clear()

    def get_summary(self) -> str:
        status = "✅ On" if self.enabled else "⏸ Off"
        return f"{status} · {len(self.memory)}/{self.max_length} turns stored"
