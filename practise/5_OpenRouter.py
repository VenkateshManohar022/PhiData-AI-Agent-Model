from phi.agent import Agent, RunResponse
from phi.model.openrouter import OpenRouter
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
agent = Agent(
    model=OpenRouter(
                    # id="google/gemma-3n-e2b-it:free", 
                    id="deepseek/deepseek-chat-v3.1:free",
                    #  max_tokens=4096, 
                     api_key=os.getenv("OPENROUTER_API_KEY"),
                     name="OpenRouter",
                     base_url="https://openrouter.ai/api/v1"
                     ),
    markdown=True
)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story.")
# print(run.content)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story.")