import os
from io import BytesIO
from time import sleep

import helium
from dotenv import load_dotenv
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from smolagents import CodeAgent, GradioUI, LiteLLMModel, Tool
from smolagents.agents import ActionStep


class SearchCtrlF(Tool):
    name = "search_item_ctrl_f"
    description = "Search for an item on the current page via Ctrl+F and jumps to the nth occurrence."
    inputs = {
        "text": {
            "type": "string",
            "description": "The text to search for.",
        },
        "nth_result": {
            "type": "int",
            "description": "Which occurrence to jump to.",
            "default": 1,
        },
    }
    output_type = "string"

    def __init__(self, driver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = driver
    
    def forward(self, text:str, nth_result:int=1) -> str:
        elements = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
        if nth_result > len(elements):
            raise Exception(f"Match n°{nth_result} not found (Only {len(elements)} occurrences found).")
        result = f"Found {len(elements)} occurrences for '{text}'."
        elem = elements[nth_result - 1]
        self.driver.execute_script("arguments[0].scrollIntoView();", elem)
        result += f"\nFocused on the {nth_result} occurrence of '{text}'."
        return result

class GoBack(Tool):
    name = "go_back"
    description = "Goes back to previous page."
    inputs = {}
    output_type = "string"

    def __init__(self, driver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = driver
    
    def forward(self) -> str:
        self.driver.back()
        return "Went back to previous page."

class ClosePopups(Tool):
    name = "close_popups"
    description = "Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows! This does not work on cookie consent banners."
    inputs = {}
    output_type = "string"

    def __init__(self, driver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = driver
    
    def forward(self) -> str:
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        return "Closed any visible modal or pop-up on the page."


def save_screenshot(current_memory_step: ActionStep, agent:CodeAgent) -> None:
    """Save the screenshot of the current page."""
    sleep(1)  # Let JS animations happen before taking the screenshot

    driver = helium.get_driver()
    current_step = current_memory_step.step_number
    if driver is not None:
        # remove previous screenshots for lean processing
        for previous_memory_step in agent.memory.steps: # steps: list of ActionStep
            if isinstance(previous_memory_step, ActionStep) and previous_memory_step.step_number < current_step:
                previous_memory_step.observations_images = None
        
        # Take a screenshot of the current page
        png_bytes = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png_bytes))
        print("Captured screenshot of the browser.")

        # Save the screenshot to the current memory step
        current_memory_step.observations_images = [image.copy()] # create a copy to make sure it persists

    # Update / Add to observations with the current url, while keeping the previous ones
    current_url_info = f"Current URL: {driver.current_url}"
    current_memory_step.observations = (
        current_url_info if current_memory_step.observations is None else current_memory_step.observations + "\n" + current_url_info
    )


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

    # Instantiate the tools
    search_ctrlf = SearchCtrlF(driver)
    go_back = GoBack(driver)
    close_popups = ClosePopups(driver)

    # Create the agent
    agent = CodeAgent(
        model=model,
        tools=[search_ctrlf, go_back, close_popups],
        additional_authorized_imports=["helium"],
        step_callbacks=[save_screenshot],
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