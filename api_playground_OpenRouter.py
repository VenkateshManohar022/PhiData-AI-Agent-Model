import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.openrouter import OpenRouter
from phi.tools.website import WebsiteTools
from phi.playground import Playground, serve_playground_app
from telegram_tool import TelegramTool, ParserTool

load_dotenv()
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

# MODAL = "llama3.1:8b"
MODAL = "deepseek/deepseek-chat-v3.1:free"
# MODAL = "google/gemma-3n-e2b-it:free"

# Initialize Telegram tool
telegram_tool = TelegramTool(
    bot_token=os.environ["BOT_TOKEN"],
    chat_id=os.environ["CHAT_ID"]
)

# --- Agent 1: Website Data Extraction ---
website_data_extraction_agent = Agent(
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
        "Extract and summarize the main textual content to under 1000 words.",
        "Do not include any URLs or formatting in the summary."
    ],
    show_tool_calls=True,
    debug_mode=True,
    monitoring=True
)

# --- Agent 2: Script Preparation (Summarize + Telegram) ---
def post_process_summary(text: str, max_words=50):
    words = text.split()
    if len(words) > max_words:
        words = words[:max_words]
    return " ".join(words)

class SummaryTelegramTool(ParserTool):
    def extract_and_send(self, response):
        # Extract text
        text = self.extract_text_from_runresponse(response)
        # Post-process summary to max 50 words
        summary = post_process_summary(text, max_words=50)
        # Send to Telegram
        # telegram_tool.send_message(summary)
        return summary

script_tool = SummaryTelegramTool()

script_preparation_agent = Agent(
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
        "Extract the main content from the input, summarize it to 50 words max, and send it to Telegram using send_message().",
        "Do NOT return Python code; execute the function call immediately."
    ],
    show_tool_calls=True,
    debug_mode=True,
    monitoring=True
)

# --- Manager Agent ---
manager_agent = Agent(
    name="Manager Agent",
    role="Coordinates website extraction and Telegram messaging",
    team=[website_data_extraction_agent, script_preparation_agent],
    model=OpenRouter(
                    id=MODAL,
                     api_key=os.getenv("OPENROUTER_API_KEY"),
                     name="OpenRouter",
                     base_url="https://openrouter.ai/api/v1",
                     allow_function_calls=True
                     ),
    instructions=[
        "Step 1: Get a URL from the user and assign it to the Website Data Extraction Agent.",
        "Step 2: Take the extracted text and pass it to the Script Preparation Agent to summarize and send to Telegram.",
        "Step 3: Confirm the summary is sent."
    ],
    show_tool_calls=True,
    debug_mode=True,
    monitoring=True
)

# --- Playground App ---
app = Playground(
    agents=[manager_agent, website_data_extraction_agent, script_preparation_agent]
).get_app()

if __name__ == "__main__":
    serve_playground_app("api_playground:app", reload=True)
