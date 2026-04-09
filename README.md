# ⚡ Electronics AI Tutor

A **local, privacy‑focused AI tutor** for electronics engineering.  
Ask questions, upload PDF textbooks, and get answers grounded in your documents — with optional web search fallback and conversation memory.

![Gradio](https://img.shields.io/badge/Gradio-5.x-blue)
![Ollama](https://img.shields.io/badge/Ollama-llama3.2%3A3b-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-yellow)

## ✨ Features

- 📚 **Local RAG** – Answers come from your uploaded PDFs (Digital Logic, Electronic Devices, etc.)
- 🌐 **Web search fallback** – Uses DuckDuckGo when documents lack an answer
- 🧠 **Conversation memory** – Remembers recent turns (toggleable, adjustable depth)
- ⚙️ **Ollama integration** – Choose any model (`llama3.2:3b`, `phi3:mini`, `mistral:7b`)
- 📂 **Incremental PDF upload** – Add new PDFs without rebuilding the whole database
- 🔄 **Full rebuild** – Re‑index all documents from scratch
- 🎨 **Modern UI** – Light/dark theme, responsive layout, source citations
- 🔐 **100% local** – No API keys, no external calls (except optional web search)

## 🖥️ Interface Preview

**Main chat view**  
![Chat interface](screenshot.png)

**Sidebar settings**  
![Sidebar](screenshot1.png)

**Settings**  
![Web search](screenshot2.png)

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Ollama** installed and running – [Download](https://ollama.com/)
- Pull at least one model (e.g., `llama3.2:3b`):
  ```bash
  ollama pull llama3.2:3b