from crewai import Crew, Task, Process
from langchain_openai import ChatOpenAI
from core.config import settings
from core.llm_cost import LLMCost
from core.logger_config import logger

from agents.fundamental_agents import (
    fundamental_analyst,
    news_analyst,
    quote_analyst,
    financial_analyst,
)

from models.fundamental_models import (
    DataSet_Metrics,
    DataSet_News,
    DataSet_EOD,
    Executive_Summary
)

# Init manager LLM with correct model + key from settings
manager_llm = ChatOpenAI(
    model=settings.model_name,
    api_key=settings.openai_api_key,
    temperature=0.2,
    max_tokens=2048,  
    max_retries=1     # Added to prevent endless retries
)

# Task Definitions
fundamental_task = Task(
    description="Extract from the {user_query}: 1. Ticker(s) 2. For each ticker, a set of financial metrics involved in addressing the user request 3. A concise analysis to answer user's question.",
    agent=fundamental_analyst,
    output_pydantic=DataSet_Metrics,
    async_execution=False,
    expected_output="A list of objects containing a ticker, a list of relevant metrics, and an executive summary."
)

news_task = Task(
    description="Extract from the {user_query}: 1. Ticker(s) 2. For each ticker, a set of recent news relating to the ticker(s) 3. A concise analysis of the companies' present situations.",
    agent=news_analyst,
    output_pydantic=DataSet_News,
    async_execution=False,
    expected_output="A list of objects containing a ticker, a list of relevant news, and a concise analysis."
)

quote_task = Task(
    description="Extract from the {user_query}: 1. Ticker(s) 2. For each ticker, the last quarter OLHCV data.",
    agent=quote_analyst,
    output_pydantic=DataSet_EOD,
    async_execution=False,
    expected_output="A list of objects containing a ticker and its OLHCV dataframe."
)

consolidation_task = Task(
    description="Answer the {user_query} by using outputs of fundamental, news and quote analysts. Provide a consolidated answer containing your financial analysis and insights according to CFA standards.",
    agent=financial_analyst,
    output_pydantic=Executive_Summary,
    async_execution=False,
    context=[fundamental_task, news_task, quote_task],
    expected_output= "Exactly ONE JSON structured response containing an executive summary, financial metrics, "
                     "news, and quote data in compliance with the provided schema.")

# Assemble the Crew
fundamental_workflow = Crew(
    agents=[
        fundamental_analyst,
        news_analyst,
        quote_analyst,
        financial_analyst
    ],
    tasks=[
        fundamental_task,
        news_task,
        quote_task,
        consolidation_task
    ],
    manager_llm=manager_llm,
    process=Process.sequential,
    verbose=True,
    memory=True
)
