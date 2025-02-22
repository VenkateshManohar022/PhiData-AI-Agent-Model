from phi.agent import Agent
from phi.tools.website import WebsiteTools  # Correct import
from phi.model.ollama import Ollama
from telegram_tool import TelegramTool  # Import the custom tool

import os
from dotenv import load_dotenv

load_dotenv()

telegram_tool = TelegramTool(
    bot_token=os.environ["BOT_TOKEN"], chat_id=os.environ["CHAT_ID"]
)


# 🚀 Website Data Extraction Agent
website_data_extraction_agent = Agent(
    name="Website Data Extraction Agent",
    role="Extract relevant data from provided website link",
    instructions=[
        "Extract relevant content from the given URL.",
        "Ensure the extracted data is structured with sections: 'History', 'Types', and 'Playing Techniques'.",
    ],
    tools=[WebsiteTools()],  # ✅ Correct tool
    model=Ollama(id="mistral"),
    debug_mode=True,
)

# 🚀 Script Preparation Agent
script_preparation_agent = Agent(
    name="Script Preparation Agent",
    role="Format extracted content for Telegram",
    instructions=[
        "Format the extracted guitar information into a structured message.",
        "Ensure the message is concise and clearly structured before sending.",
    ],
    model=Ollama(id="mistral"),
    debug_mode=True,
)

# 🚀 Telegram Sending Agent
telegram_sending_agent = Agent(
    name="Telegram Sending Agent",
    role="Send messages to Telegram",
    instructions=["Send the formatted message to Telegram."],
    tools=[telegram_tool],  # ✅ Correct tool
    model=Ollama(id="mistral"),
    debug_mode=True,
)

# 🚀 Manager Agent (Fixing Task Execution)
manager_agent = Agent(
    name="Manager Agent",
    team=[
        website_data_extraction_agent,
        script_preparation_agent,
        telegram_sending_agent,
    ],
    model=Ollama(id="mistral"),
    instructions=[
        "Step 1: Extract data from the given website URL using the Website Data Extraction Agent.",
        "Step 2: Format the extracted data using the Script Preparation Agent.",
        "Step 3: Send the formatted data to Telegram using the Telegram Sending Agent.",
        "Step 4: Display the extracted data here.",
    ],
    debug_mode=True,
    show_tool_calls=True,
    markdown=True,
)

# 🚀 Step-by-Step Execution
url = "https://en.wikipedia.org/wiki/Guitar"

# Step 1: Extract Data from Website
extracted_data = website_data_extraction_agent.run(input={"url": url})

# Step 2: Format Data for Telegram
formatted_data = script_preparation_agent.run(input={"text": extracted_data})

# Step 3: Send Data to Telegram
telegram_sending_agent.run(input={"message": formatted_data})

# Step 4: Display Extracted Data
print("🔹 Extracted Data:")
print(extracted_data)
