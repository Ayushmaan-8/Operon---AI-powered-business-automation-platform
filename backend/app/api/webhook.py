from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import Lead
from app.services.ai_engine import analyze_lead
from app.services.reply_engine import generate_reply
from app.services.action_engine import decide_action
from app.schemas.lead_schema import AIDecisionResponse
from app.database.models import AIDecision, ActionLog

router = APIRouter(prefix="/webhook", tags=["whatsapp"])


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    try:
        # Extract message (Meta format)
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "no_message"}

        msg = messages[0]

        phone = msg.get("from")
        text = msg.get("text", {}).get("body", "")

        # 1. Save lead
        db_lead = Lead(
            name=phone,  # temporary
            phone=phone,
            source="whatsapp",
            message=text
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)

        # 2. AI Analysis
        try:
            decision_data = analyze_lead(
                lead_name=phone,
                lead_message=text
            )
        except:
            decision_data = AIDecisionResponse(
                intent="unknown",
                lead_score=50,
                category="medium",
                confidence=0.5,
                reasoning="fallback"
            )

        # Save AI decision
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

        # 3. Action
        action_data = decide_action(decision_data)

        db_action = ActionLog(
            lead_id=db_lead.id,
            action=action_data["action"],
            priority=action_data["priority"],
            reason=action_data["reason"]
        )
        db.add(db_action)
        db.commit()

        # 4. Generate reply
        reply = generate_reply(
            lead_name=phone,
            lead_message=text,
            intent=decision_data.intent,
            category=decision_data.category
        )

        db_lead.reply = reply
        db.commit()

        # ⚡ (Step 3.2 will send this back to WhatsApp)

        return {"status": "processed"}

    except Exception as e:
        return {"error": str(e)}