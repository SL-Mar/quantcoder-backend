from pydantic import BaseModel, Field
from typing import List

# === Chat with Fundamentals / Chat Entry ===

class UserQuery(BaseModel):
    user_query: str = Field(..., description="User's raw input.")

# === EOD / Quote Data ===

class OLHCV(BaseModel): 
    Date: str
    Open: float
    Low: float
    High: float
    Close: float
    AdjClose: float
    Volume: int

class EODResult(BaseModel):
    ticker: str
    data: List[OLHCV]

class DataSet_EOD(BaseModel):
    DataSet: List[EODResult] = Field(..., description="A list of EOD dataframes for each ticker.")


# === News Data ===

class Fin_News(BaseModel):
    Ticker: str
    Date: str
    Title: str
    Content: str
    Link: str

class Set_News(BaseModel):
    Ticker: str
    News: List[Fin_News]
    Present: str

class DataSet_News(BaseModel):
    DataSet: List[Set_News] = Field(..., description="A list of news for each ticker.")


# === Financial Metrics ===

class Fin_Metric(BaseModel):
    Ticker: str
    Metric: str
    Value: str

class Set_Metrics(BaseModel):
    Ticker: str
    Metrics: List[Fin_Metric]
    State: str

class DataSet_Metrics(BaseModel):
    DataSet: List[Set_Metrics] = Field(..., description="A list of metrics for each ticker.")


# === Final Consolidated Output ===

class Executive_Summary(BaseModel):
    Tickers: List[str] = Field(..., description="Companies tickers.")
    Ex_summary: str = Field(..., description="Executive summary.")
    Metrics: DataSet_Metrics
    News: DataSet_News
    Quote: DataSet_EOD
