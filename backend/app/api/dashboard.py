from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.database.session import get_db
from app.database.models import Lead, AIDecision, ActionLog
from app.utils.monitoring import log_event, log_error

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

# Define response schemas for clean JSON responses
class DashboardLeadItem(BaseModel):
    id: str
    name: Optional[str]
    email: Optional[str]
    source: Optional[str]
    status: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardAnalyticsResponse(BaseModel):
    total_leads: int
    new_leads: int
    high_priority: int
    medium_priority: int
    low_priority: int

@router.get("/leads", response_model=List[DashboardLeadItem])
def get_dashboard_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    log_event("dashboard_fetch_leads_request", {"skip": skip, "limit": limit})
    try:
        leads = db.query(Lead).order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()
        return leads
    except Exception as e:
        log_error("dashboard_db_query_error", {"endpoint": "/leads", "error": str(e)})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/leads/{id}")
def get_dashboard_lead_detail(id: str, db: Session = Depends(get_db)):
    try:
        lead = db.query(Lead).filter(Lead.id == id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
            
        ai_decision = db.query(AIDecision).filter(AIDecision.lead_id == id).first()
        action_log = db.query(ActionLog).filter(ActionLog.lead_id == id).first()
        
        return {
            "lead": {
                "id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "phone": lead.phone,
                "source": lead.source,
                "business_type": lead.business_type,
                "service_requested": lead.service_requested,
                "budget": lead.budget,
                "message": lead.message,
                "context_summary": lead.context_summary,
                "status": lead.status,
                "reply": lead.reply,
                "created_at": lead.created_at.isoformat() if lead.created_at else None
            },
            "ai_decision": {
                "id": ai_decision.id,
                "intent": ai_decision.intent,
                "lead_score": ai_decision.lead_score,
                "category": ai_decision.category,
                "confidence": ai_decision.confidence,
                "reasoning": ai_decision.reasoning,
                "created_at": ai_decision.created_at.isoformat() if ai_decision.created_at else None
            } if ai_decision else None,
            "action": {
                "id": action_log.id,
                "action": action_log.action,
                "priority": action_log.priority,
                "reason": action_log.reason,
                "created_at": action_log.created_at.isoformat() if action_log.created_at else None
            } if action_log else None
        }
    except HTTPException:
        raise
    except Exception as e:
        log_error("dashboard_db_query_error", {"endpoint": f"/leads/{id}", "error": str(e)})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/analytics", response_model=DashboardAnalyticsResponse)
def get_dashboard_analytics(db: Session = Depends(get_db)):
    log_event("dashboard_fetch_analytics_request")
    try:
        total_leads = db.query(Lead).count()
        new_leads = db.query(Lead).filter(Lead.status == "new").count()
        
        high_priority = db.query(ActionLog).filter(ActionLog.priority == "high").count()
        medium_priority = db.query(ActionLog).filter(ActionLog.priority == "medium").count()
        low_priority = db.query(ActionLog).filter(ActionLog.priority == "low").count()
        
        return DashboardAnalyticsResponse(
            total_leads=total_leads,
            new_leads=new_leads,
            high_priority=high_priority,
            medium_priority=medium_priority,
            low_priority=low_priority
        )
    except Exception as e:
        log_error("dashboard_db_query_error", {"endpoint": "/analytics", "error": str(e)})
        raise HTTPException(status_code=500, detail="Internal server error")
