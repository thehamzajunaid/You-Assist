from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []
    use_knowledge_base: bool = False

class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: Optional[int] = None
    sources: Optional[List[dict]] = None

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class DocumentInfo(BaseModel):
    id: UUID
    filename: str
    chunks: int