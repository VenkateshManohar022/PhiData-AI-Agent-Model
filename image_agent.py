import requests

# Download the image and save it locally
# image_url = "https://upload.wikimedia.org/wikipedia/commons/b/bf/Krakow_-_Kosciol_Mariacki.jpg"
image_url = "https://en.wikipedia.org/wiki/Thomas_Edison#/media/File:Thomas_Edison2.jpg"
image_path = "images/krakow.jpg"

response = requests.get(image_url)
with open(image_path, "wb") as file:
    file.write(response.content)

# Now, use the local image file
from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.duckduckgo import DuckDuckGo

agent = Agent(
    model=Ollama(id="mistral"),
    tools=[DuckDuckGo()],
    markdown=True,
)

agent.print_response(
    "Tell me about this image and give me the latest news about it.",
    images=[image_path],  # Pass local file
    stream=True,
)
