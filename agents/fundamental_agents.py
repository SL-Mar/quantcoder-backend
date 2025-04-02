from crewai import Agent, LLM
from tools.EODHDTool import EODHDTool
from tools.EODHDNewsTool import EODHDNewsTool
from tools.EODTool import EODTool


fundamental_analyst = Agent(
    role="Fundamental analyst",
    goal="Collect and analyze fundamental data for one or more specified companies.",
    backstory="A virtual financial analyst conversant with CFA or FINRA financial analysis standards.",
    verbose=True,
    max_iter = 1,
    tools=[EODHDTool()],
)

news_analyst = Agent(
    role="News analyst",
    goal="Collect and analyze the most recent news for one specific company.",
    backstory="A virtual seasoned financial news analyst.",
    verbose=True,
    max_iter = 1,
    tools=[EODHDNewsTool()],
)

quote_analyst = Agent(
    role="Quote analyst",
    goal="Collect and analyze the most recent olhcv for one specific company.",
    backstory="A virtual seasoned financial analyst specialised in price action interpretation.",
    verbose=True,
    max_iter = 1,
    tools=[EODTool()],
)

financial_analyst = Agent(
    role="Financial analyst",
    goal="Consolidate data and views provided by the fundamental, news and quote analysts.",
    backstory="A virtual seasoned chartered financial analyst specializing in US Equities.",
    max_iter = 1,
    verbose=True,
    tools=[],
)
