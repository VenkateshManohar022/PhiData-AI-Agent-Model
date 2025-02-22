from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.website import WebsiteTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools import Tool
import json

from phi.playground import Playground, serve_playground_app
from telegram_tool import TelegramTool, ParserTool  # Import the custom tool

# from telegram_tool import FormatResponseParser  # Import the custom tool

import os
from dotenv import load_dotenv

load_dotenv()

# telegram_tool = TelegramTool(bot_token=os.environ['BOT_TOKEN'], chat_id=os.environ['CHAT_ID'])

# Define extract_text_tool as a Phidata Tool


telegram_tool = TelegramTool(
    bot_token=os.environ["BOT_TOKEN"], chat_id=os.environ["CHAT_ID"]
)

# Set a static website link for the agent to scrape
website_link = "https://en.wikipedia.org/wiki/Stock"

# Define the Website Data Extraction Agent
website_data_extraction_agent = Agent(
    name="Website Data Extraction Agent",
    role="Extract relevant data from provided website link",
    model=Ollama(id="mistral"),
    tools=[WebsiteTools()],
    instructions=[
        f"Scrape and extract data from the provided website link. The user will provide the URL."
    ],  # Using the hardcoded link here
    # instructions=[f"Scrape and extract data from the provided website link: {website_link}."],  # Using the hardcoded link here
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    debug_mode=True,
)

script_preparation_agent = Agent(
    name="Script Preparation Agent",
    role="Send messages to Telegram",
    model=Ollama(id="mistral", allow_function_calls=True),
    tools=[ParserTool(),telegram_tool],  # Keep this, now it will detect `send_message()`
    instructions=[
        "Extract meaningful content from the RunResponse object.",
        "Convert it to a formatted string with a maximum of 50 words.",
        "Send the formatted message to Telegram using `send_message`.",
        "Do NOT return Python code—execute the function immediately.",
    ],
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    debug_mode=True,
)

# script_preparation_agent.run("Test Data")
print("Tools _ SCRIPT : ", script_preparation_agent.tools)
# telegram_tool.send_message("🚀 Hello from Phidata!")

manager_agent = Agent(
    name="Manager Agent",
    team=[website_data_extraction_agent, script_preparation_agent],
    model=Ollama(id="mistral"),
    instructions=[
        "Step 1: Extract data from the given website URL using the Website Data Extraction Agent.",
        "Step 2: Format the extracted data using the Script Preparation Agent.",
        "Step 3: Send the Script.",
    ],
    debug_mode=True,
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
)


# response = website_data_extraction_agent.run(input="https://github.com/emarco177/ice_breaker/tree/2-search-agent-finish")
# print("Agent_1 : ", response)
# def send_to_telegram(data):
#     message = f"Extracted Data on Guitar:\n\n{data}"
#     telegram_tool.send_message(message)  # Directly send message
#     print("✅ Message sent to Telegram!")



# def extract_text_from_runresponse(response):
#     if hasattr(response, "content"):
#         return str(response.content)
#     elif isinstance(response, list):
#         return "\n".join(str(item.content) for item in response if hasattr(item, "content"))
#     elif isinstance(response, dict):
#         return str(response.get("content", ""))
#     return str(response)


# def manager_workflow():
#     print("Step 1: Extracting data from website...")
#     extracted_data = website_data_extraction_agent.run(
#         "https://en.wikipedia.org/wiki/Guitar"
#     )

#     print("Data Type :", type(extracted_data))
#     # Example usage:
#     text_data = extract_text_from_runresponse(extracted_data)  # Assuming 'response' is your RunResponse object
#     print('ConversionType : '+text_data + " -------END ------")


#     print(" Step 2: Formatting and Sending to Telegram...")
#     script_preparation_agent.run(text_data)  # Merged agent handles both tasks

#     print(" Step 3: Displaying extracted data")
#     return text_data


# # Run manager workflow manually
# manager_workflow()

app = Playground(
    agents=[manager_agent, website_data_extraction_agent, script_preparation_agent]
).get_app()

if __name__ == "__main__":
    serve_playground_app("api_playground:app", reload=True)
