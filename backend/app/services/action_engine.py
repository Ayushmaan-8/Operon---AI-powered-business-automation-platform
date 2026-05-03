from app.schemas.decision_schema import AIDecisionResponse

def decide_action(ai_decision):
    score = ai_decision.lead_score

    if score >= 80:
        return {
            "action": "immediate_call",
            "priority": "high",
            "reason": "High value lead (80+ score)"
        }

    elif score >= 50:
        return {
            "action": "mark_followup",
            "priority": "medium",
            "reason": "Moderate quality lead (50–79)"
        }

    else:
        return {
            "action": "add_to_nurture_sequence",
            "priority": "low",
            "reason": "Low intent lead (<50)"
        }
