"""
Electronics AI Tutor - Shared Data Models
"""
from dataclasses import dataclass
from typing import Any


@dataclass
class ProcessResult:
    """Standardized result object for operations"""
    success: bool
    message: str
    data: Any = None

    def __str__(self):
        return self.message
