import logging
import requests
from phi.tools import Tool, Toolkit
from pydantic import Field

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)



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
        Extract meaningful content from a RunResponse object.
        Ensures the message does not exceed 50 words.
        """
        try:
            # Check if response has "text" or any other relevant attribute
            if isinstance(response, dict) and "text" in response:
                message = response["text"]
            elif hasattr(response, "text"):
                message = response.text
            else:
                message = str(response)  # Fallback to string conversion

            # Limit message length
            words = message.split()
            trimmed_message = " ".join(words[:50])

            print("Debug: Formatted message ->", trimmed_message)  # Debugging
            return trimmed_message

        except Exception as e:
            print("Error in format_run_response:", str(e))
            return "Error formatting response"

    def send_message(self, message) -> str:
        """
        Sends a message to the configured Telegram chat.
        """
        try:
            print("Debug: Original message type ->", type(message))

            # Ensure it's formatted correctly before sending
            if not isinstance(message, str):
                message = self.format_run_response(message)

            print("Debug: Sending formatted message ->", message)

            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": message}
            response = requests.post(url, json=payload).json()

            print("Debug: Telegram API Response ->", response)

            if response.get("ok"):
                return response["result"]["text"]  # Return the sent message
            else:
                return f"Telegram API Error: {response.get('description', 'Unknown error')}"

        except Exception as e:
            print("Error in send_message:", str(e))
            return f"Exception in send_message: {str(e)}"
