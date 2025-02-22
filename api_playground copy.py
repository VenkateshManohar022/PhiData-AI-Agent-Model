from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.website import WebsiteTools
from phi.tools.duckduckgo import DuckDuckGo

from phi.playground import Playground, serve_playground_app
from telegram_tool import TelegramTool  # Import the custom tool

import os
from dotenv import load_dotenv

load_dotenv()

# telegram_tool = TelegramTool(bot_token=os.environ['BOT_TOKEN'], chat_id=os.environ['CHAT_ID'])

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
    tools=[telegram_tool],  # Keep this, now it will detect `send_message()`
    instructions=[
        "Use the 'send_message' function from 'Telegram Tool' to send messages.",
        "Ensure the function is executed instead of returning Python code.",
    ],
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    debug_mode=True,
)

# script_preparation_agent.run("Test Data")
print("Tools _ SCRIPT : ", script_preparation_agent.tools)
# telegram_tool.send_message(" Hello from Phidata!")

# Create Manager Agent
manager_agent = Agent(
    name="Manager Agent",
    team=[website_data_extraction_agent, script_preparation_agent],
    instructions=[
        " Step 1: Extracting data from website...",
        "Step 2: Sending the extarcted data to Telegram...",
    ],
    model=Ollama(id="mistral"),
    debug_mode=True,
)

# manager_agent.print_response("extract data : https://en.wikipedia.org/wiki/Guitar and send it", stream=True)
# manager_agent.run()


# Run Playground for testing purposes
# app = Playground(agents=[manager_agent, website_data_extraction_agent, script_preparation_agent]).get_app()
# app = Playground(agents=[manager_agent, website_data_extraction_agent, script_preparation_agent]).get_app()

# if __name__ == "__main__":
#     serve_playground_app("api_playground:app", reload=True)














# script_preparation_agent = Agent(
#     name="Script Preparation Agent",
#     model=Ollama(id="llama3.2"),
#     tools=[ParserTool(), telegram_tool],
#     # output_parser=FormatResponseParser(),
#     structured_outputs=True,
#     instructions=[
#         "Extract meaningful content from the RunResponse object.",
#         "Convert it to a formatted string with a maximum of 50 words.",
#         "Send the formatted message to Telegram using `send_message`.",
#         "Do NOT return Python code—execute the function immediately.",
#     ],
#     debug_mode=True,
# )

# manager_agent = Agent(
#     name="Manager Agent",
#     team=[website_data_extraction_agent, script_preparation_agent],
#     model=Ollama(id="llama3.2"),
#     instructions=[
#         "Step 1: Extract data from the given website URL using the Website Data Extraction Agent.",
#         "Step 2: Format the extracted data using the Script Preparation Agent.",
#         "Step 3: Send the Script.",
#     ],
#     debug_mode=True,
#     show_tool_calls=True,
#     markdown=True,
#     monitoring=True,
# )
