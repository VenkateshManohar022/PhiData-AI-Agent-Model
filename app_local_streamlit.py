import streamlit as st
from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.website import WebsiteTools
from telegram_tool import TelegramTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Telegram tool
telegram_tool = TelegramTool(
    bot_token=os.environ["BOT_TOKEN"], chat_id=os.environ["CHAT_ID"]
)

# Define Website Data Extraction Agent
website_data_extraction_agent = Agent(
    name="Website Data Extraction Agent",
    role="Extract relevant data from provided website link",
    model=Ollama(id="mistral"),
    tools=[WebsiteTools()],
    instructions=[
        "Scrape and extract data from the provided website link.",
        "Creating a Marketing Script with proper structure",
        "Ignore Python Code and just summarize the Marketing content in short"
    ],
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    debug_mode=True,
)

def extract_text_from_runresponse(response):
    if response is None:
        return ""
    if hasattr(response, "content"):
        return str(response.content)
    elif isinstance(response, list):
        return "\n".join(str(item.content) for item in response if hasattr(item, "content"))
    elif isinstance(response, dict):
        return str(response.get("content", ""))
    return str(response)

# Streamlit UI
st.title("Website Data Extraction & Telegram Sender")

website_link = st.text_input("Enter Website URL:", "https://www.thinkwithgoogle.com/intl/en-apac/consumer-insights/consumer-trends/e-conomy-sea-2024/")

if st.button("Extract & Send Data"):
    st.write("**Step 1: Extracting data from website...**")
    extracted_data = website_data_extraction_agent.run(website_link)
    text_data = extract_text_from_runresponse(extracted_data)
    
    st.write("**Step 2: Sending to Telegram...**")
    telegram_tool.send_message(text_data)
    
    st.write("**Step 3: Displaying Extracted Marketing Data:**")
    st.text_area("Extracted Data:", text_data, height=300)