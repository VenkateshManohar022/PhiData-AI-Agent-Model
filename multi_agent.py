from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

from dotenv import load_dotenv

load_dotenv()

# Define the Website Data Extraction Agent
website_data_extraction_agent = Agent(
    name="Website Data Extraction Agent",
    role="Get financial data",
    model=Ollama(id="mistral"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)
    ],
    instructions=["Fetch real-time stock data and financial details for NVDA."],
    show_tool_calls=True,
    markdown=True,
)

# Define the Script Preparation Agent for web searches
script_preparation_agent = Agent(
    name="Script Preparation Agent",
    role="Search the web for information",
    model=Ollama(id="mistral"),
    tools=[DuckDuckGo()],
    instructions=["Search for the latest news related to NVDA and provide summaries."],
    show_tool_calls=True,
    markdown=True,
)

# Define the Manager Agent (Coordinates the work between other agents)
manager_agent = Agent(
    team=[website_data_extraction_agent, script_preparation_agent],
    name="Manager Agent",
    model=Ollama(id="mistral"),
    instructions=[
        "Collect results from both agents and combine them into a final response."
    ],
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
    debug_mode=True,
)

# Fetch financial data from the Website Data Extraction Agent
financial_data = website_data_extraction_agent.print_response(
    "Get the stock price and analyst recommendations for NVDA", stream=False
)

# Fetch the latest news from the Script Preparation Agent
news_data = script_preparation_agent.print_response(
    "Search for the latest news about NVDA", stream=False
)

# Combine the responses
final_response = (
    f"Financial Data for NVDA:\n{financial_data}\n\nLatest News for NVDA:\n{news_data}"
)

# Print the final combined response
print(final_response)


"""OUTPUT TO VIEW IN CONSOLE"""

# Ensure Manager Agent triggers the actions for real data retrieval (not just steps)
response = manager_agent.print_response(
    "Summarize analyst recommendations and share the latest news for NVDA",  # This blocks the Playground execution SO currently Executing it...
    stream=True,  # Disable stream for immediate results
)
print("Final Response :::", response)
