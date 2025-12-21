from pydantic import BaseModel
from typing import List, Dict


class QueryRequest(BaseModel):
    question: str
    top_k: int = 8


class QueryResponse(BaseModel):
    answer: str
    contexts: List[Dict]
