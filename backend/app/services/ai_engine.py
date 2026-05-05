import os
import json
import logging
import re
from groq import Groq
from app.schemas.decision_schema import AIDecisionResponse
from app.core.config import settings
from app.utils.monitoring import log_event, log_error

logger = logging.getLogger(__name__)

URGENCY_WORDS = ["asap", "urgent", "immediately", "within a week", "today"]


def analyze_lead(lead_name: str, lead_message: str) -> AIDecisionResponse:
    log_event("ai_request_start", {"lead_name": lead_name})

    if not settings.GROQ_API_KEY:
        log_event("ai_fallback_triggered", {"reason": "API key not configured"})
        return AIDecisionResponse(
            intent="Fallback",
            lead_score=50,
            category="medium",
            confidence=0.5,
            reasoning="Fallback: API key not configured"
        )

    try:
        client = Groq(api_key=settings.GROQ_API_KEY)

        system_prompt = """
        You are an AI lead analyst for a business automation platform.

        Your job is to analyze an inbound lead and return a STRICT JSON object with:
        intent, lead_score, category, confidence, reasoning

        DO NOT rely only on budget.

        Evaluate using:
        - Intent clarity (clear need for automation)
        - Urgency (timeline words like ASAP, within a week)
        - Specificity (mentions of workflow, product, use-case)
        - Budget (optional supporting signal)

        Scoring model (total 100):
        - Clear intent: +30
        - Urgency: +40
        - Budget mentioned: +20
        - Specific details: +10

        Priority mapping rules:

        - HIGH:
            strong intent + urgency

        - MEDIUM:
            clear intent but no urgency
            OR budget discussion without urgency

        - LOW:
            vague, unclear, or irrelevant message

        IMPORTANT:
            - A clear request for automation MUST NOT be classified as low.
            - If intent is clear but urgency is missing → classify as MEDIUM even if score is low.

        Rules:
        - Urgency can override missing budget
        - Budget alone should NOT make a lead high priority
        - Vague messages must be low priority
        - Always ensure score matches category
        - If unsure, lower confidence instead of guessing

        Output format (STRICT JSON ONLY):
        {
            "intent": "short label",
            "lead_score": number,
            "category": "low | medium | high",
            "confidence": number between 0 and 1,
            "reasoning": "brief explanation referencing signals"
        }
        """

        user_prompt = f"""
        Analyze this lead:

        Name: {lead_name}
        Message: {lead_message}

        Return JSON only.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )

        result_text = response.choices[0].message.content

        # safer JSON extraction
        match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in AI response")

        # Parse JSON
        result_dict = json.loads(match.group())

        # ✅ Ensure ALL required fields exist
        result_dict.setdefault("intent", "unknown")
        result_dict.setdefault("lead_score", 0)
        result_dict.setdefault("category", "low")
        result_dict.setdefault("confidence", 0.5)
        result_dict.setdefault("reasoning", "No reasoning provided")

        # ✅ Normalize confidence
        try:
            result_dict["confidence"] = float(result_dict["confidence"])
        except:
            result_dict["confidence"] = 0.5

        # 🔥 Backend urgency boost (small but powerful)
        message_lower = lead_message.lower()
        if any(word in message_lower for word in URGENCY_WORDS):
            result_dict["lead_score"] = min(100, result_dict.get("lead_score", 0) + 10)
            
        # Force medium if intent is clear but score too low
        if result_dict.get("intent", "").lower() != "unknown" and result_dict["lead_score"] < 40:
            result_dict["category"] = "medium"
            result_dict["lead_score"] = max(result_dict["lead_score"], 50)

        # Re-map category after adjustment
        score = result_dict.get("lead_score", 0)
        if score >= 80:
            result_dict["category"] = "high"
        elif score >= 40:
            result_dict["category"] = "medium"
        else:
            result_dict["category"] = "low"

        log_event("ai_response_received", {
            "intent": result_dict.get("intent"),
            "score": result_dict.get("lead_score"),
            "category": result_dict.get("category")
        })

        return AIDecisionResponse(**result_dict)

    except Exception as e:
        log_error("ai_error", {"error": str(e)})
        log_event("ai_fallback_triggered", {"reason": f"Exception: {str(e)}"})
        return AIDecisionResponse(
            intent="Fallback",
            lead_score=50,
            category="medium",
            confidence=0.5,
            reasoning="Fallback due to error"
        )