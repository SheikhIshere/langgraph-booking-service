from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    requires_human: bool

class MessageOut(BaseModel):
    role: str
    content: str

class HistoryResponse(BaseModel):
    conversation_id: str
    messages: List[MessageOut]
