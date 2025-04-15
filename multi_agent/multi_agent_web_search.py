import argparse
import os
import re

import requests
from dotenv import load_dotenv
from markdownify import markdownify
from requests.exceptions import RequestException

from smolagents import CodeAgent, DuckDuckGoSearchTool, GradioUI, LiteLLMModel, ToolCallingAgent, tool


"""
              +----------------+
              | Manager agent  |
              +----------------+
                       |
        _______________|______________
       |                              |
Code Interpreter            +------------------+
    tool                    | Web Search agent |
                            +------------------+
                               |            |
                        Web Search tool     |
                                   Visit webpage tool
"""

## Web Agent


@tool
def visit_webpage(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Convert the HTML content to Markdown
        markdown_content = markdownify(response.text).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content

    except RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def parse_args():
    help_msg = """Multi Agent Web Search"""
    parser = argparse.ArgumentParser(description=help_msg, formatter_class=argparse.RawTextHelpFormatter)
    # Essential Args
    # For anthropic: change args below to 'LiteLLM', 'anthropic/claude-3-5-sonnet-20240620' and "ANTHROPIC_API_KEY"
    parser.add_argument("--model_src", type=str, default="LiteLLM", choices=["HfApi", "LiteLLM", "Transformers"])
    parser.add_argument("--model", type=str, default="gemini/gemini-2.0-flash")
    parser.add_argument("--LiteLLMModel_API_key_name", type=str, default="GEMINI_API_KEY")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    # Choose which LLM engine to use!
    if args.model_src == "HfApi":
        from smolagents import HfApiModel

        # You can choose to not pass any model_id to HfApiModel to use a default free model
        model = HfApiModel(model_id=args.model, token=os.environ.get("HF_API_KEY"))

    elif args.model_src == "Transformers":
        from smolagents import TransformersModel

        model = TransformersModel(model_id=args.model)

    elif args.model_src == "LiteLLM":
        model = LiteLLMModel(model_id=args.model, api_key=os.environ.get(args.LiteLLMModel_API_key_name))
    else:
        raise ValueError('Choose the models source from ["HfApi", "LiteLLM", "Transformers"]')

    # Web browsing is a single-timeline task that does not require parallel tool calls,
    # so JSON tool calling works well for that. We thus choose a ToolCallingAgent.
    web_agent = ToolCallingAgent(
        tools=[DuckDuckGoSearchTool(), visit_webpage],
        model=model,
        max_steps=10,
        # since sometimes web search requires exploring many pages before finding the correct answer,
        # we prefer to increase the number of max_steps to 10.
        name="web_search_agent",
        description="Runs web searches for you.",
        # we gave this agent attributes name and description, mandatory attributes
        # to make this agent callable by its manager agent.
    )

    ## Manager Agent
    manager_agent = CodeAgent(
        tools=[],
        model=model,
        managed_agents=[web_agent],
        additional_authorized_imports=["time", "numpy", "pandas"]
    )

    GradioUI(manager_agent).launch()
    # try: "If LLM training continues to scale up at the current rhythm until 2030, what would be the electric power in GW required to power the biggest training runs by 2030? What would that correspond to, compared to some countries? Please provide a source for any numbers used."
    # agent_output = manager_agent.run(task="If LLM training continues to scale up at the current rhythm until 2030, what would be the electric power in GW required to power the biggest training runs by 2030? What would that correspond to, compared to some countries? Please provide a source for any numbers used.")
    # print("Final output:\n", agent_output)


if __name__ == "__main__":
    load_dotenv()
    main()
