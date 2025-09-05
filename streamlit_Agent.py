import os
import time
from queue import Queue
from threading import Thread
from dotenv import load_dotenv
import streamlit as st
from phi.agent import Agent
from phi.model.openrouter import OpenRouter
from phi.tools.website import WebsiteTools
from telegram_tool import TelegramTool, ParserTool
from phi.playground import Playground, serve_playground_app

# ----------------------
# Load environment
# ----------------------
load_dotenv()
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

MODAL = "deepseek/deepseek-chat-v3.1:free"

# ----------------------
# Initialize Telegram tool
# ----------------------
telegram_tool = TelegramTool(
    bot_token=os.environ["BOT_TOKEN"],
    chat_id=os.environ["CHAT_ID"]
)

# ----------------------
# Logging setup
# ----------------------
# We'll use a Queue for each agent to stream logs to the frontend
agent_logs = {
    "Website Data Extraction Agent": Queue(),
    "Script Preparation Agent": Queue(),
    "Manager Agent": Queue()
}

def log(agent_name, message):
    """Add log message to agent's queue"""
    agent_logs[agent_name].put(message)

# ----------------------
# Helper: Stream logs to Streamlit
# ----------------------
def display_agent_logs(agent_name):
    """Display logs for an agent in Streamlit"""
    placeholder = st.empty()
    logs_list = []
    while True:
        try:
            log_message = agent_logs[agent_name].get(timeout=0.5)
            logs_list.append(log_message)
            placeholder.text("\n".join(logs_list))
        except:
            time.sleep(0.1)

# ----------------------
# Agent Classes
# ----------------------
def post_process_summary(text: str, max_words=50):
    words = text.split()
    if len(words) > max_words:
        words = words[:max_words]
    return " ".join(words)

class SummaryTelegramTool(ParserTool):
    def extract_and_send(self, response):
        text = self.extract_text_from_runresponse(response)
        summary = post_process_summary(text, max_words=50)
        log("Script Preparation Agent", f"Summary generated: {summary}")
        # telegram_tool.send_message(summary)
        return summary

# ----------------------
# Define Agents
# ----------------------
website_agent = Agent(
    name="Website Data Extraction Agent",
    role="Scrape relevant content from website",
    model=OpenRouter(
        id=MODAL,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        allow_function_calls=True
    ),
    tools=[WebsiteTools()],
    instructions=[
        "Scrape the website URL provided by the user.",
        "Extract and summarize the main textual content."
    ],
    show_tool_calls=True,
    debug_mode=True,
    monitoring=True
)

script_tool = SummaryTelegramTool()
script_agent = Agent(
    name="Script Preparation Agent",
    role="Summarize text and send to Telegram",
    model=OpenRouter(
        id=MODAL,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        allow_function_calls=True
    ),
    tools=[script_tool, telegram_tool],
    instructions=[
        "Summarize text to 50 words max and send to Telegram."
    ],
    show_tool_calls=True,
    debug_mode=True,
    monitoring=True
)

manager_agent = Agent(
    name="Manager Agent",
    role="Coordinates website extraction and Telegram messaging",
    team=[website_agent, script_agent],
    model=OpenRouter(
        id=MODAL,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        allow_function_calls=True
    ),
    instructions=[
        "Step 1: Get a URL from the user and assign it to the Website Agent.",
        "Step 2: Pass extracted text to Script Agent to summarize and send to Telegram.",
        "Step 3: Confirm the summary is sent."
    ],
    show_tool_calls=True,
    debug_mode=True,
    monitoring=True
)

# ----------------------
# Streamlit UI
# ----------------------
st.title("🌐 PhiData Agent Visualization")
st.subheader("Agent Monitoring Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://img.icons8.com/color/48/000000/web.png", width=50)
    st.subheader("Website Agent")
    Thread(target=display_agent_logs, args=("Website Data Extraction Agent",), daemon=True).start()

with col2:
    st.image("https://img.icons8.com/color/48/000000/script.png", width=50)
    st.subheader("Script Agent")
    Thread(target=display_agent_logs, args=("Script Preparation Agent",), daemon=True).start()

with col3:
    st.image("https://img.icons8.com/color/48/000000/manager.png", width=50)
    st.subheader("Manager Agent")
    Thread(target=display_agent_logs, args=("Manager Agent",), daemon=True).start()

# ----------------------
# User Input
# ----------------------
url_input = st.text_input("Enter website URL to process:")

if st.button("Run Agents"):
    def run_agents():
        log("Manager Agent", f"Starting workflow for URL: {url_input}")
        # Simulate workflow
        extracted_text = "Simulated website text extraction..."
        log("Website Data Extraction Agent", f"Extracted text: {extracted_text}")
        summary = post_process_summary(extracted_text, max_words=50)
        log("Script Preparation Agent", f"Summary: {summary}")
        log("Manager Agent", "Workflow completed successfully.")

    Thread(target=run_agents, daemon=True).start()