import streamlit as st
import openai
import requests
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from phi.flow import Flow

# Set API keys
OPENAI_API_KEY = "your_openai_api_key"
TELEGRAM_BOT_API_KEY = "your_telegram_bot_api_key"
TELEGRAM_CHAT_ID = "your_chat_id"


# Website Data Extraction Agent
def extract_website_content(url):
    """Simulated website extraction (Replace with real scraper)."""
    return f"Extracted content from {url}"  # Placeholder content


website_extraction_tool = Tool(
    name="Website Data Extraction Agent",
    func=extract_website_content,
    description="Extracts content from a given website link.",
)


# Script Preparation Agent
def generate_marketing_script(extracted_text):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a marketing expert."},
            {
                "role": "user",
                "content": f"Generate a marketing script based on this:\n{extracted_text}",
            },
        ],
    )
    return response["choices"][0]["message"]["content"]


script_preparation_tool = Tool(
    name="Script Preparation Agent",
    func=generate_marketing_script,
    description="Generates a marketing script using GPT-4.",
)


# Telegram Messaging Function
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    return response.status_code == 200


# Manager Agent (Orchestrator)
def manager_agent(website_link):
    extracted_text = website_extraction_tool.run(website_link)
    marketing_script = script_preparation_tool.run(extracted_text)
    success = send_to_telegram(marketing_script)
    return marketing_script, success


# Streamlit UI
st.title("AI Marketing Agent Team")
website_link = st.text_input("Enter Website Link:")

if st.button("Generate Marketing Script"):
    if website_link:
        marketing_script, success = manager_agent(website_link)
        if success:
            st.success("Marketing Script Sent to Telegram!")
            st.text_area("Generated Script:", marketing_script, height=200)
        else:
            st.error("Failed to send the message. Check Telegram API credentials.")
    else:
        st.warning("Please enter a valid website link.")
