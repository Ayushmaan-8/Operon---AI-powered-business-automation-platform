from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import EmailStr

class LeadCreate(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    phone: str
    service_requested: str
    budget: Optional[str] = None
    message: str
    source: Optional[str] = None
    business_type: Optional[str] = None

class LeadResponse(BaseModel):
    id: str
    name: Optional[str]
    email: EmailStr
    phone: Optional[str]
    source: Optional[str]
    business_type: Optional[str]
    service_requested: Optional[str]
    budget: Optional[str]
    message: Optional[str]
    context_summary: Optional[str] # This field is reserved for future summarization and conversation context extraction using AI.
    status: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
