# Browser Automation VLM Agent

This project implements a **Browser Automation Vision-Language Model (VLM) Agent** using `smolagents`. It provides tools to automate web browsing tasks, such as navigating web pages, searching for content, handling popups, and extracting information. The agent is equipped with a **Gradio UI** for seamless interaction and supports multiple LLM providers.

## Features
- **Web Automation**: Navigate to web pages, click on elements, and search within pages.
- **Popup Handling**: Close modals and popups with ease.
- **Information Extraction**: Extract and process webpage content.
- **Screenshot Capture**: Automatically captures screenshots during interactions.
- **LLM Support**: Works with models from `LiteLLM`, `HfApi`, and `Transformers`.
- **Gradio UI**: Interactive web interface for user interaction.

## Tools
The agent provides the following tools:
- **`search_item_ctrl_f`**: Searches for a specific text on the current page and focuses on the nth occurrence.
- **`go_back`**: Navigates back to the previous page.
- **`close_popups`**: Closes visible modals or popups on the page.
- **helium itself**

## Quick Start
- Clone the repo.
- Install [uv](https://docs.astral.sh/uv/), as the project manager.
- Run the following command:
```bash
cd browser_auto_agent
uv run [browser_auto_vlm_agent.py]
```

## Example Use Cases
You can modify the system to be effective for tasks like:
- Data extraction from websites
- Web research automation
- UI testing and verification
- Content monitoring

## License
See `LICENSE` for details.

## Contributing
Contributions are welcome! Feel free to open issues and submit pull requests. 🚀