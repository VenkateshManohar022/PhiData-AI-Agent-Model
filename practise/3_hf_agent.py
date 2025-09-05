from phi.agent import Agent, RunResponse
from phi.model.huggingface import HuggingFaceChat
from dotenv import load_dotenv
import os
load_dotenv()
# Set your Hugging Face token as an environment variable or directly here
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

agent = Agent(
    model=HuggingFaceChat(
        # id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        id="meta-llama/Meta-Llama-3-8B-Instruct",
        allow_function_calls=True,
        name="HuggingFaceChat",
        provider="huggingface",
    ),
    markdown=True
)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story.")
# print(run.content)

# Print the response on the terminal
agent.print_response("Share a 2 sentence horror story.")