# Multi-Agent Web Search

This project implements a **Multi-Agent Web Search** system using `smolagents`. It features a manager agent that oversees a web search agent, capable of retrieving relevant information from the web. The system uses **DuckDuckGo search** and a **webpage visitor tool** to fetch and process webpage content into Markdown format.

## Features
- **Multi-Agent Architecture**: Includes a manager agent and a web search agent.
- **Web Search & Scraping**: Uses DuckDuckGo for searching and retrieves webpage content.
- **LLM Support**: Works with models from `LiteLLM`, `HfApi`, and `Transformers`.
- **Gradio UI**: Interactive web interface for seamless user interaction.

## Installation
Ensure you have Python 3.8+ installed. Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

Set up your API key by creating a `.env` file:

```bash
echo "GROQ_API_KEY=your_api_key_here" > .env
```

## Quick Start
Run the following command to start the Multi-Agent Web Search system:

```bash
python main.py --model_src LiteLLM --model groq/qwen-2.5-coder-32b
```

### What Happens?
1. **Web Agent:** Searches DuckDuckGo and retrieves relevant webpage content.
2. **Manager Agent:** Oversees the web agent and processes the data.
3. **Gradio UI:** Launches an interactive interface for user queries.

## Usage
Once the system is running, you can:
- Ask complex web search questions.
- Retrieve summarized content from visited pages.
- Leverage AI-powered search assistance.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Contributing
Feel free to submit issues and pull requests! 🚀

