from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.website import WebsiteTools
from telegram_tool import TelegramTool, ParserTool  # Import the custom tool

import os
from dotenv import load_dotenv

load_dotenv()

telegram_tool = TelegramTool(
    bot_token=os.environ["BOT_TOKEN"], chat_id=os.environ["CHAT_ID"]
)



# Define the Website Data Extraction Agent
website_data_extraction_agent = Agent(
    name="Website Data Extraction Agent",
    role="Extract relevant data from provided website link",
    model=Ollama(id="mistral"),
    tools=[WebsiteTools()],
    instructions=[
        f"Scrape and extract data from the provided website link. The user will provide the URL.",
        "Creating a Marketing Script with proper structure",
        "Ignore Python Code and just summarize the Marketing conetnt in short"
    ],  # Using the hardcoded link here
    # instructions=[f"Scrape and extract data from the provided website link: {website_link}."],  # Using the hardcoded link here
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    debug_mode=True,
)


# response = website_data_extraction_agent.run(input="https://github.com/emarco177/ice_breaker/tree/2-search-agent-finish")
# print("Agent_1 : ", response)
# def send_to_telegram(data):
#     message = f"Extracted Data on Guitar:\n\n{data}"
#     telegram_tool.send_message(message)  # Directly send message
#     print("✅ Message sent to Telegram!")



def extract_text_from_runresponse(response):
    """
        Extracts meaningful content from a PhiRunner response.

        Args:
            response (Any): The response object to process.

        Returns:
            str: Extracted text.
        """
    if response is None:
        return ""
    if hasattr(response, "content"):
        return str(response.content)
    elif isinstance(response, list):
        return "\n".join(str(item.content) for item in response if hasattr(item, "content"))
    elif isinstance(response, dict):
        return str(response.get("content", ""))
    return str(response)

#Hardcoded Agents..
# Set a static website link for the agent to scrape
# website_link = "https://en.wikipedia.org/wiki/Stock"
# website_link="https://sproutsocial.com/insights/tiktok-ban/"
website_link="https://www.thinkwithgoogle.com/intl/en-apac/consumer-insights/consumer-trends/e-conomy-sea-2024/"

def manager_workflow():
    print("Step 1: Extracting data from website...")
    extracted_data = website_data_extraction_agent.run(
        website_link
    )

    print("Data Type :", type(extracted_data))
    # # Example usage:
    text_data = extract_text_from_runresponse(extracted_data)  # Assuming 'response' is your RunResponse object
    print("Data Type :", type(text_data))
    print('ConversionType : '+text_data + " -------END ------")


    print(" Step 2: Formatting and Sending to Telegram...")
    telegram_tool.send_message(text_data)  # Merged agent handles both tasks

    print(" Step 3: Displaying Marketing Scripted data")
    return text_data


# Run manager workflow manually
manager_workflow()
