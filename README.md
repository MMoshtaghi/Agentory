# Agentory

This repository contains two **LLM-powered agent systems** for information retrieval and web search. These systems leverage **LLMs**, **semantic search**, and **web scraping** to enhance knowledge discovery and retrieval.

## Projects in This Repository

### 1️⃣ Agentic Retrieval-Augmented Generation (RAG)
A **retrieval-augmented generation** system that utilizes **ChromaDB** for efficient document retrieval and **LLM-based query response**.

📌 **Features:**
- Embeds and indexes documents using `HuggingFace` embeddings.
- Uses `ChromaDB` for vector-based semantic search.
- Supports multiple LLM providers: `LiteLLM`, `HfApi`, `Transformers`.
- Interactive **Gradio UI** for easy interaction.

📂 **Find more details in the [Agentic RAG directory](./agentic_rag/README.md).**

---

### 2️⃣ Multi-Agent Web Search
A **multi-agent system** that performs **web searches** and retrieves **webpage content** for better query understanding.

📌 **Features:**
- Uses `DuckDuckGo` search to find relevant web pages.
- Converts webpage content into Markdown format for readability.
- A **manager agent** oversees the **web search agent**.
- Interactive **Gradio UI** for seamless user interaction.

📂 **Find more details in the [Multi-Agent directory](./multi_agent/README.md).**

---

## Installation
Each project has its own installation guide and dependencies. Navigate to the respective directories and follow the instructions in their `README.md` files.

## License
See `LICENSE` for more details.

## Contributing
Contributions are welcome! Feel free to open issues and submit pull requests. 🚀

