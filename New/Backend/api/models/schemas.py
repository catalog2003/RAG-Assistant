from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class UploadResponse(BaseModel):
    status: str
    document: str
    chunks_created: int
    message: Optional[str] = None

class Source(BaseModel):
    document: str
    page: int
    score: Optional[float] = None

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = "default"

class AskResponse(BaseModel):
    answer: str
    sources: List[Source]
    processing_time: float

class ChatMessage(BaseModel):
    role: str
    message: str
    timestamp: datetime

class HistoryResponse(BaseModel):
    session_id: str
    messages: List[ChatMessage]

class HealthResponse(BaseModel):
    status: str
    version: str
    index_loaded: bool
    embedding_model: str
    llm_model: str