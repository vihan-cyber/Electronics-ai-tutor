# Electronics AI Tutor

A local RAG-based tutor for electronics, using Ollama, ChromaDB, and Gradio.

## Features
- Upload PDF textbooks
- Ask questions with document retrieval
- Web search fallback (DuckDuckGo)
- Conversation memory
- Dark/light theme

## Setup
1. Install Ollama and pull a model: `ollama pull llama3.2:3b`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # Linux/macOS
# or .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt