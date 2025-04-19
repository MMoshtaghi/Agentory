# Agentory

This repository contains two **LLM-powered agent systems** for information retrieval and web search. These systems leverage **LLMs**, **semantic search**, and **web scraping** to enhance knowledge discovery and retrieval.

## Projects in This Repository

### 1️⃣ Agentic Retrieval-Augmented Generation (RAG)
A **retrieval-augmented generation** system that utilizes **ChromaDB** for efficient document retrieval.

📌 **Features:**
- Embeds and indexes documents.
- Uses `ChromaDB` for vector-based semantic search.
- Supports multiple LLM providers: `LiteLLM`, `HfApi`, `Transformers`.
- Interactive **Gradio UI** for easy interaction.

📂 **Find more details in the [Agentic RAG directory](./agentic_rag/README.md).**

---

### 2️⃣ Multi-Agent Web Search
A **multi-agent system** that performs **web searches** and retrieves **webpage content** for basde on user's query.

📌 **Features:**
- Uses `DuckDuckGo` search API to find relevant web pages.
- Converts webpage content into Markdown format for readability.
- A **manager agent** oversees the **web search agent**.
- Supports multiple LLM providers: `LiteLLM`, `HfApi`, `Transformers`.
- Interactive **Gradio UI** for seamless user interaction.

📂 **Find more details in the [Multi-Agent directory](./multi_agent/README.md).**

---

### 3️⃣ Browser Automation VLM Agent
A **Browser Automation Vision-Language Model (VLM) Agent** that automates web browsing tasks, such as navigating web pages, searching for content, handling popups, and extracting information.

📌 **Features:**
- **Web Automation**: Navigate to web pages, click on elements, and search within pages.
- **Popup Handling**: Close modals and popups with ease.
- **Information Extraction**: Extract and process webpage content.
- **Screenshot Capture**: Automatically captures screenshots during interactions.
- **LLM Support**: Works with models from `LiteLLM`, `HfApi`, and `Transformers`.
- **Gradio UI**: Interactive web interface for user interaction.

📂 **Find more details in the [Browser Automation directory](./browser_auto_agent/README.md).**

---

## Quick Start
- Clone the repo.
- [uv](https://docs.astral.sh/uv/) is recommended for easy install and setup for all agents in this repo. You only need run each script in their directory (`uv` will create the venv and install all the dependencies for you).

### Agentic RAG
```bash
cd agentic_rag
uv run agentic_rag_chromadb.py
```

### Multi-Agent Web Search
```bash
cd multi_agent
uv run multi_agent_web_search.py
```

### Browser Automation VLM Agent
```bash
cd browser_auto_agent
uv run browser_auto_vlm_agent.py
```

## License
See `LICENSE` for more details.

## Contributing
Contributions are welcome! Feel free to open issues and submit pull requests. 🚀

