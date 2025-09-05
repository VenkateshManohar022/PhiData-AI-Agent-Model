import os
import time
from dotenv import load_dotenv
import gradio as gr
from phi.agent import Agent
from phi.model.openrouter import OpenRouter
from phi.tools.website import WebsiteTools
from telegram_tool import TelegramTool, ParserTool

load_dotenv()
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
MODAL = "deepseek/deepseek-chat-v3.1:free"

# ----------------------
# Initialize Telegram tool
# ----------------------
telegram_tool = TelegramTool(
    bot_token=os.getenv("BOT_TOKEN"),
    chat_id=os.getenv("CHAT_ID")
)

# ----------------------
# Logs storage
# ----------------------
agent_logs = {
    "Website": "",
    "Script": "",
    "Manager": ""
}

# ----------------------
# Helpers
# ----------------------
def log(agent_name, message):
    agent_logs[agent_name] += message + "\n"

def post_process_summary(text: str, max_words=50):
    words = text.split()
    if len(words) > max_words:
        words = words[:max_words]
    return " ".join(words)

class SummaryTelegramTool(ParserTool):
    def extract_and_send(self, response):
        text = self.extract_text_from_runresponse(response)
        if not text.strip():
            return ""
        summary = post_process_summary(text, max_words=50)
        log("Script", f"Concise summary: {summary}")
        telegram_tool.send_message(summary)
        return summary

# ----------------------
# Agents
# ----------------------
website_agent = Agent(
    name="Website Agent",
    role="Scrape website content",
    model=OpenRouter(
        id=MODAL,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        allow_function_calls=True
    ),
    tools=[WebsiteTools()],
    instructions=[
        "Scrape website content and generate initial summary (max 1000 words)"
    ],
    show_tool_calls=True,
    debug_mode=True,
    monitoring=True
)

script_tool = SummaryTelegramTool()
script_agent = Agent(
    name="Script Agent",
    role="Concise summary & Telegram",
    model=OpenRouter(
        id=MODAL,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        allow_function_calls=True
    ),
    tools=[script_tool, telegram_tool],
    instructions=[
        "Take website summary, generate concise summary (50 words max), and send to Telegram"
    ],
    show_tool_calls=True,
    debug_mode=True,
    monitoring=True
)

manager_agent = Agent(
    name="Manager Agent",
    role="Coordinate workflow",
    team=[website_agent, script_agent],
    model=OpenRouter(
        id=MODAL,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        allow_function_calls=True
    ),
    instructions=["Coordinate website extraction and concise summary generation"],
    show_tool_calls=True,
    debug_mode=True,
    monitoring=True
)

# ----------------------
# Workflow generator for streaming
# ----------------------
def run_agents_stream(url):
    log("Manager", f"Workflow started for URL: {url}")
    yield agent_logs["Manager"], agent_logs["Website"], agent_logs["Script"]

    # Web agent extracts and summarizes
    log("Website", "Extracting website content...")
    extracted_text = f"Simulated content extracted from {url}"
    log("Website", f"Initial summary: {post_process_summary(extracted_text, max_words=1000)}")
    yield agent_logs["Manager"], agent_logs["Website"], agent_logs["Script"]
    time.sleep(1)

    # Script agent generates concise summary and sends to Telegram
    concise_summary = post_process_summary(extracted_text, max_words=50)
    log("Script", f"Concise summary sent to Telegram: {concise_summary}")
    telegram_tool.send_message(concise_summary)
    yield agent_logs["Manager"], agent_logs["Website"], agent_logs["Script"]
    time.sleep(1)

    log("Manager", "Workflow completed successfully.")
    yield agent_logs["Manager"], agent_logs["Website"], agent_logs["Script"]

# ----------------------
# Gradio interface
# ----------------------
with gr.Blocks() as demo:
    gr.Markdown("# 🌐 PhiData Multi-Agent Workflow")
    url_input = gr.Textbox(label="Website URL", placeholder="https://example.com")
    run_button = gr.Button("Run Agents")

    with gr.Row():
        manager_output = gr.Textbox(label="Manager Logs", interactive=False)
        website_output = gr.Textbox(label="Website Logs", interactive=False)
        script_output = gr.Textbox(label="Script Logs", interactive=False)

    run_button.click(
        fn=run_agents_stream,
        inputs=url_input,
        outputs=[manager_output, website_output, script_output],
        stream=True  # <-- enables Playground-like streaming
    )

demo.launch()