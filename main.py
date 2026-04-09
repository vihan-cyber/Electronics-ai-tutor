"""
Electronics AI Tutor - Entry Point
Run: python main.py
"""
import os
import logging

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import gradio as gr
from ui import create_ui, CSS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Starting Electronics AI Tutor")
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        theme=gr.themes.Base(),   # Base theme — our CSS overrides everything
        css=CSS,
        favicon_path="favicon.ico" if os.path.exists("favicon.ico") else None,
    )
