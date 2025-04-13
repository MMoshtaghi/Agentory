import os

import helium
from dotenv import load_dotenv
from PIL import Image
from selenium import webdriver

from smolagents import CodeAgent, GradioUI, LiteLLMModel, Tool


def parse_args():
    import argparse
    help_msg = """Browser Automation VLM Agent"""
    parser = argparse.ArgumentParser(help_msg, formatter_class=argparse.RawTextHelpFormatter)
    # Essential Args
    # For anthropic: change args below to 'LiteLLM', 'anthropic/claude-3-5-sonnet-20240620' and "ANTHROPIC_API_KEY"
    parser.add_argument("--model_src", type=str, default="LiteLLM", choices=["HfApi", "LiteLLM", "Transformers"])
    parser.add_argument("--model", type=str, default="groq/qwen-2.5-coder-32b")
    parser.add_argument("--LiteLLMModel_API_key_name", type=str, default="GROQ_API_KEY")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.browser == "chrome":
        # Configure Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--force-device-scale-factor=1")
        chrome_options.add_argument("--window-size=1000,1350")
        chrome_options.add_argument("--window-position=0,0")
        chrome_options.add_argument("--disable-pdf-viewer")

        # Start Chrome with the specified options
        driver = helium.start_chrome(headless=False, options=chrome_options)
    elif args.browser == "firefox":
        raise NotImplementedError("Firefox is not supported yet.")
    else:
        raise ValueError('Choose the browser from ["chrome", "firefox"]')


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

    

    # Create the agent
    agent = CodeAgent(
        model=model,
        tools=[],
        additional_authorized_imports=["helium"],
        step_callbacks=[],
        max_steps=20,
        verbosity_level=2,
    )

    # import helium for the agent to use
    agent.python_executor("from helium import *", agent.state)

    agent_output = agent.run(task="TBD")
    print("Final output:\n", agent_output)


if __name__ == "__main__":
    load_dotenv()
    main()