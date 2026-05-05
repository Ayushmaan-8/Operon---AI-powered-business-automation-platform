import uuid
from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey, Text
from sqlalchemy.sql import func
from app.database.session import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    source = Column(String, nullable=True) # form / whatsapp
    business_type = Column(String, nullable=True)
    service_requested = Column(String, nullable=True)
    budget = Column(String, nullable=True)
    message = Column(String, nullable=True)
    context_summary = Column(String, nullable=True) # This field is reserved for future summarization and conversation context extraction using AI.
    status = Column(String, default="new")
    reply = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AIDecision(Base):
    __tablename__ = "ai_decisions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False)
    intent = Column(String, nullable=True)
    lead_score = Column(Integer, nullable=True)
    category = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    reasoning = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False)
    action = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
