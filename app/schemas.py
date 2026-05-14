from datetime import datetime
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1)


class AnalyzeResponse(BaseModel):
    result: str
    score: float


class HistoryItem(BaseModel):
    id: int
    input_text: str
    result_text: str
    score: float | None
    model_name: str
    created_at: datetime

    class Config:
        from_attributes = True
