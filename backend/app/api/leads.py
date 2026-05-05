from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database.session import get_db
from app.database.models import Lead, AIDecision, ActionLog
from app.schemas.lead_schema import LeadCreate, LeadResponse
from app.services.ai_engine import analyze_lead
from app.services.action_engine import decide_action
from app.schemas.lead_schema import AIDecisionResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/leads", tags=["leads"])

@router.post("/form", response_model=LeadResponse)
def create_lead_form(lead_in: LeadCreate, db: Session = Depends(get_db)):

    # 1. Save lead
    db_lead = Lead(
        name=lead_in.name,
        email=lead_in.email,
        phone=lead_in.phone,
        source=lead_in.source or "form",
        business_type=lead_in.business_type,
        service_requested=lead_in.service_requested,
        budget=lead_in.budget,
        message=lead_in.message
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    from app.services.reply_engine import generate_reply

    # 2. AI Analysis (LLM #1)
    try:
        decision_data = analyze_lead(
            lead_name=db_lead.name or "",
            lead_message=db_lead.message or ""
        )

    except Exception as e:
        logger.error(f"AI analysis failed for lead {db_lead.id}: {e}")

        # fallback (VERY IMPORTANT)
        decision_data = AIDecisionResponse(
            intent="unknown",
            lead_score=50,
            category="medium",
            confidence=0.5,
            reasoning="Fallback due to AI failure"
        )
    
    print("DECISION:", decision_data)

    # 3. Save AI decision
    db_decision = AIDecision(
        lead_id=db_lead.id,
        intent=decision_data.intent,
        lead_score=decision_data.lead_score,
        category=decision_data.category,
        confidence=decision_data.confidence,
        reasoning=decision_data.reasoning
    )
    db.add(db_decision)
    db.commit()

    print("AI SAVED")
    print("SAVED AI DECISION:", db_decision)

    # 4. Decide action
    try:
        action_data = decide_action(decision_data)

        db_action = ActionLog(
            lead_id=db_lead.id,
            action=action_data["action"],
            priority=action_data["priority"],
            reason=action_data["reason"]
        )
        db.add(db_action)
        db.commit()

    except Exception as e:
        logger.error(f"Action processing failed for lead {db_lead.id}: {e}")

    # 5. Generate reply (LLM #2) ✅ CORRECT PLACE
    try:
        reply_text = generate_reply(
            lead_name=db_lead.name or "",
            lead_message=db_lead.message or "",
            intent=decision_data.intent,
            category=decision_data.category
        )
    except Exception as e:
        logger.error(f"Reply generation failed: {e}")
        reply_text = None

    db_lead.reply = reply_text
    db.commit()
    db.refresh(db_lead)
    return db_lead
    
@router.get("", response_model=List[LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()
    return leads

@router.get("/{id}")
def get_lead(id: str, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    ai_decision = db.query(AIDecision).filter(AIDecision.lead_id == id).first()
    action_log = db.query(ActionLog).filter(ActionLog.lead_id == id).first()
    
    reply = lead.reply

    return {
        "lead": lead,
        "ai_decision": ai_decision,
        "action": action_log,
        "reply": reply
    }
 