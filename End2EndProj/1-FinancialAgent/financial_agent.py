from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

import os
from dotenv import load_dotenv
load_dotenv()

Groq.api_key = os.getenv("GROQ_API_KEY")

# Check if the GROQ_API_KEY is set
if not Groq.api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables")

##  Web serach agent
web_serach_agent = Agent(
    name="Web Search Agent",
    role="Search the web for information",
    model=Groq(id="llama3-70b-8192"),
    tools=[DuckDuckGo()],
    instructions=["Always include source"],
    show_tool_calls=True,
    markdown=True
)

## Financial agent
financial_agent = Agent(
    name="Financial Agent",
    role="Gather financial data",
    model=Groq(id="llama3-70b-8192"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    show_tool_calls=True,
    markdown=True
)

multi_ai_agent = Agent(
    team=[web_serach_agent, financial_agent],
    model=Groq(id="llama3-70b-8192"),
    instructions=["Always include source", "User table to display the data"],
    show_tool_calls=True,
    markdown=True
)

multi_ai_agent.print_response("Summarize analyst recommendations and share the latest new for NVDA", stream=True)