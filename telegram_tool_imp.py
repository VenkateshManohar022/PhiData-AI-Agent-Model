import logging
import requests
from phi.tools import Tool, Toolkit
from pydantic import Field

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

from typing import Any

class ParserTool(Toolkit):
    """
    Parser tool to extract text from PhiRunner response objects.
    """

    def __init__(self):
        super().__init__(name="Parser Tool")  # Initialize toolkit
        self.register(self.extract_text_from_runresponse)  # Register function

    def extract_text_from_runresponse(self, response: Any) -> str:
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

        if isinstance(response, dict):
            return str(response.get("content", ""))

        if isinstance(response, list):
            return "\n".join(
                str(getattr(item, "content", item)) for item in response
            )

        return str(response)


class TelegramTool(Toolkit):
    bot_token: str = Field(..., description="Telegram Bot Token")
    chat_id: str = Field(..., description="Telegram Chat ID")

    def __init__(self, bot_token: str, chat_id: str):
        super().__init__(name="Telegram Tool")  # Removed 'type' argument

        self.bot_token = bot_token
        self.chat_id = chat_id

        self.register(self.send_message)  # Register the function

    def format_run_response(self, response):
        """
        Converts a RunResponse object into a formatted string message.
        Ensures the message does not exceed 50 words.
        """
        if hasattr(response, "text"):
            message = response.text  # Extract the main content
        else:
            message = str(response)  # Fallback to string conversion

        # Limit the message to 50 words
        words = message.split()
        trimmed_message = " ".join(words[:50])

        return trimmed_message

    def send_message(self, message: str) -> str:
        """
        Sends a message to the configured Telegram chat.
        """
        # Assume `run_response` is the object returned by the agent
        message = self.format_run_response(message)
        print("message||message : ", message)

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message}
        response = requests.post(url, json=payload).json()

        if response.get("ok"):
            print("Telegram_pass")
            return response["result"]["text"]  # Return the sent message
        else:
            print("Telegram_fail")
            return f"Telegram API Error: {response.get('description', 'Unknown error')}"
