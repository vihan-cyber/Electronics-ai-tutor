"""
Electronics AI Tutor - UI
Premium Gradio 6 interface. Light theme by default, toggleable to dark.
"""
import gradio as gr
from config import Config
from memory import ConversationMemory
from ui_callbacks import UICallbacks

CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');

:root {
  --bg:           #f5f7fb;
  --surface:      #ffffff;
  --surface2:     #f0f2f8;
  --border:       #dde1ec;
  --accent:       #2563eb;
  --text:         #111827;
  --text-muted:   #6b7280;
  --danger:       #dc2626;
  --radius:       14px;
  --radius-sm:    8px;
  --mono:         'DM Mono', monospace;
  --head:         'Syne', sans-serif;
  --body:         'Lora', Georgia, serif;
  --shadow:       0 1px 4px rgba(0,0,0,0.08);
  --shadow-md:    0 4px 16px rgba(0,0,0,0.10);
}

:root[data-theme="dark"] {
  --bg:           #0f1117;
  --surface:      #181c27;
  --surface2:     #1e2335;
  --border:       #2a2f45;
  --accent:       #4f8ef7;
  --text:         #e8ecf4;
  --text-muted:   #6b7280;
  --shadow:       0 1px 4px rgba(0,0,0,0.4);
  --shadow-md:    0 4px 16px rgba(0,0,0,0.5);
}

*, *::before, *::after { box-sizing: border-box; }

body, .gradio-container {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--body) !important;
  transition: background 0.3s, color 0.3s;
}

.gradio-container {
  max-width: 1480px !important;
  margin: 0 auto !important;
  padding: 0 !important;
}

footer { display: none !important; }

#header-area {
  padding: 32px 48px 18px;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(180deg, rgba(37,99,235,0.05) 0%, transparent 100%);
}

#header-area h1 {
  font-family: var(--head) !important;
  font-size: 1.9rem !important;
  font-weight: 800 !important;
  letter-spacing: -0.03em !important;
  color: var(--text) !important;
  margin: 0 !important;
}

#header-area p {
  font-family: var(--mono) !important;
  font-size: 0.75rem !important;
  color: var(--accent) !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  margin: 5px 0 0 !important;
}

#main-row {
  padding: 24px 48px 40px;
  gap: 28px;
  align-items: flex-start;
}

#chatbot-wrap .chatbot {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  height: 540px !important;
  font-family: var(--body) !important;
  box-shadow: var(--shadow-md) !important;
}

#chatbot-wrap .message.user {
  background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
  border-radius: 14px 14px 4px 14px !important;
  color: #ffffff !important;
}

#chatbot-wrap .message.bot {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px 14px 14px 4px !important;
  color: var(--text) !important;
}

#question-input textarea {
  background: var(--surface) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text) !important;
  font-family: var(--body) !important;
  font-size: 0.97rem !important;
  padding: 14px 16px !important;
  transition: border-color 0.2s, box-shadow 0.2s;
  resize: none !important;
}
#question-input textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
  outline: none !important;
}
#question-input label {
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  color: var(--text-muted) !important;
}

.btn-send {
  background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
  color: white !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--head) !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  box-shadow: 0 2px 10px rgba(37,99,235,0.25) !important;
  transition: transform 0.15s, box-shadow 0.15s !important;
}
.btn-send:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 18px rgba(37,99,235,0.38) !important; }

.btn-web {
  background: linear-gradient(135deg, #059669, #047857) !important;
  color: white !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--head) !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  box-shadow: 0 2px 10px rgba(5,150,105,0.2) !important;
  transition: transform 0.15s !important;
}
.btn-web:hover { transform: translateY(-1px) !important; }

.btn-clear {
  background: transparent !important;
  color: var(--text-muted) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--mono) !important;
  font-size: 0.82rem !important;
  transition: border-color 0.2s, color 0.2s !important;
}
.btn-clear:hover { border-color: var(--danger) !important; color: var(--danger) !important; }

#sidebar {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 20px !important;
  box-shadow: var(--shadow-md) !important;
}

.panel-label {
  font-family: var(--mono) !important;
  font-size: 0.68rem !important;
  font-weight: 500 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.12em !important;
  color: var(--text-muted) !important;
  margin-bottom: 10px !important;
  display: block;
}

#sidebar label {
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  color: var(--text-muted) !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
}

#sidebar input[type="range"] { accent-color: var(--accent) !important; }
#sidebar input[type="checkbox"] { accent-color: var(--accent) !important; }

.btn-sidebar {
  background: var(--surface2) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--mono) !important;
  font-size: 0.78rem !important;
  padding: 8px 12px !important;
  width: 100% !important;
  margin-top: 6px !important;
  transition: border-color 0.2s, background 0.2s !important;
}
.btn-sidebar:hover { border-color: var(--accent) !important; background: rgba(37,99,235,0.07) !important; }

.btn-danger-sm {
  background: transparent !important;
  color: var(--danger) !important;
  border: 1px solid rgba(220,38,38,0.35) !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--mono) !important;
  font-size: 0.75rem !important;
  padding: 6px 10px !important;
  transition: background 0.2s !important;
}
.btn-danger-sm:hover { background: rgba(220,38,38,0.08) !important; }

#status-display, #memory-status, #upload-status {
  font-family: var(--mono) !important;
  font-size: 0.76rem !important;
  color: var(--text-muted) !important;
  line-height: 1.5 !important;
}
#status-display {
  padding: 10px 12px !important;
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
}
#memory-status { color: var(--accent) !important; margin-top: 6px !important; }

.sidebar-divider { border: none; border-top: 1px solid var(--border); margin: 14px 0; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
"""


def create_ui() -> gr.Blocks:
    """Create the Gradio UI for the Electronics AI Tutor."""
    memory = ConversationMemory(max_length=Config.DEFAULT_MEMORY_LENGTH)

    with gr.Blocks(title="Electronics AI Tutor", theme=gr.themes.Base()) as demo:

        with gr.Column(elem_id="app-shell"):

            # Header
            with gr.Column(elem_id="header-area"):
                gr.HTML("""
                <h1>⚡ Electronics AI Tutor</h1>
                <p>Local RAG · Web Search · Conversation Memory · Ollama LLM</p>
                """)

            # Main content
            with gr.Row(elem_id="main-row", equal_height=False):

                # ── Chat column ──────────────────────────────
                with gr.Column(scale=3, elem_id="chatbot-wrap"):
                    chatbot = gr.Chatbot(
                        height=540,
                        show_label=False,
                        placeholder=(
                            "<div style='text-align:center;color:#9ca3af;"
                            "font-family:DM Mono,monospace;font-size:0.85rem;"
                            "padding-top:160px'>Ask anything about electronics…</div>"
                        ),
                    )
                    msg = gr.Textbox(
                        label="Your question",
                        lines=2,
                        max_lines=5,
                        placeholder="e.g. Explain how a MOSFET amplifier works…",
                        elem_id="question-input",
                    )
                    with gr.Row():
                        send_btn  = gr.Button("📨  Ask (local docs)", variant="primary",   elem_classes="btn-send",  scale=3)
                        web_btn   = gr.Button("🌐  Search Web",        variant="secondary", elem_classes="btn-web",   scale=2)
                        clear_btn = gr.Button("✕  Clear",                                   elem_classes="btn-clear", scale=1)

                # ── Sidebar ──────────────────────────────────
                with gr.Column(scale=1, elem_id="sidebar"):

                    gr.HTML('<span class="panel-label">📂 Documents</span>')
                    upload_file   = gr.File(label="Upload PDF", file_types=[".pdf"])
                    upload_status = gr.Markdown("", elem_id="upload-status")

                    gr.HTML('<hr class="sidebar-divider">')
                    gr.HTML('<span class="panel-label">⚙️ Settings</span>')
                    model_dropdown = gr.Dropdown(
                        choices=["llama3.2:3b", "phi3:mini", "mistral:7b"],
                        value=Config.DEFAULT_MODEL,
                        label="LLM Model",
                        interactive=True,
                    )
                    k_slider = gr.Slider(minimum=1, maximum=10, step=1, value=Config.RETRIEVAL_K, label="Chunks to retrieve")
                    web_fallback = gr.Checkbox(label="Auto web fallback when no local results", value=False)

                    gr.HTML('<hr class="sidebar-divider">')
                    gr.HTML('<span class="panel-label">💾 Conversation Memory</span>')
                    mem_enabled   = gr.Checkbox(label="Enable memory", value=Config.DEFAULT_MEMORY_ENABLED)
                    mem_length    = gr.Slider(minimum=1, maximum=Config.MAX_MEMORY_LENGTH, step=1, value=Config.DEFAULT_MEMORY_LENGTH, label="Memory depth (turns)")
                    mem_status    = gr.Markdown(memory.get_summary(), elem_id="memory-status")
                    clear_mem_btn = gr.Button("🗑 Clear Memory", size="sm", elem_classes="btn-danger-sm")

                    gr.HTML('<hr class="sidebar-divider">')
                    gr.HTML('<span class="panel-label">🔧 Actions</span>')
                    rebuild_btn   = gr.Button("⚙️  Full Rebuild",     elem_classes="btn-sidebar")
                    dark_mode_btn = gr.Button("🌓  Toggle Dark Mode", elem_classes="btn-sidebar")

                    gr.HTML('<hr class="sidebar-divider">')
                    gr.HTML('<span class="panel-label">ℹ️ Status</span>')
                    status_display = gr.Markdown("Initializing…", elem_id="status-display")

        # State management
        mem_state = gr.State(memory)

        # Event handlers
        send_btn.click(
            UICallbacks.chat_local,
            inputs=[msg, chatbot, mem_state, web_fallback],
            outputs=[msg, chatbot]
        ).then(
            lambda m: m.get_summary(),
            inputs=mem_state,
            outputs=mem_status
        )

        msg.submit(
            UICallbacks.chat_local,
            inputs=[msg, chatbot, mem_state, web_fallback],
            outputs=[msg, chatbot]
        ).then(
            lambda m: m.get_summary(),
            inputs=mem_state,
            outputs=mem_status
        )

        web_btn.click(
            UICallbacks.chat_web,
            inputs=[msg, chatbot, mem_state],
            outputs=[msg, chatbot]
        ).then(
            lambda m: m.get_summary(),
            inputs=mem_state,
            outputs=mem_status
        )

        clear_btn.click(
            UICallbacks.clear_chat,
            inputs=mem_state,
            outputs=[chatbot, mem_status]
        )

        upload_file.change(
            UICallbacks.upload_pdf,
            inputs=upload_file,
            outputs=upload_status
        )

        model_dropdown.change(
            UICallbacks.update_model,
            inputs=model_dropdown,
            outputs=status_display
        )

        k_slider.change(
            UICallbacks.update_k,
            inputs=k_slider,
            outputs=status_display
        )

        rebuild_btn.click(
            UICallbacks.rebuild_kb,
            outputs=status_display
        )

        mem_enabled.change(
            UICallbacks.toggle_memory,
            inputs=[mem_enabled, mem_state],
            outputs=mem_status
        )

        mem_length.change(
            UICallbacks.update_memory_length,
            inputs=[mem_length, mem_state],
            outputs=mem_status
        )

        clear_mem_btn.click(
            UICallbacks.clear_memory,
            inputs=mem_state,
            outputs=mem_status
        )

        dark_mode_btn.click(None, None, None, js="""() => {
            const root = document.documentElement;
            if (root.getAttribute('data-theme') === 'dark') {
                root.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
            } else {
                root.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            }
        }""")

        demo.load(None, None, None, js="""() => {
            if (localStorage.getItem('theme') === 'dark') {
                document.documentElement.setAttribute('data-theme', 'dark');
            }
        }""")

        demo.load(UICallbacks.startup, outputs=status_display)

    return demo