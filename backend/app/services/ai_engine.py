import os
import json
import logging
import re
from groq import Groq
from app.schemas.decision_schema import AIDecisionResponse
from app.core.config import settings
from app.utils.monitoring import log_event, log_error

logger = logging.getLogger(__name__)

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

        Analyze the lead and return ONLY valid JSON with:

        - intent
        - lead_score (0-100)
        - category (low | medium | high)
        - confidence (0-1)
        - reasoning

        Be concise, professional, and business-oriented in reasoning.
        Avoid obvious explanations like "this is a greeting".
        Focus on business intent and conversion potential.

        Scoring guideline:
        - Budget + urgency → 80+
        - Clear service need → 60–80
        - Vague interest → 40–60
        - No intent → <40

        Always ensure:
        - lead_score matches category:
            low: 0–49
            medium: 50–79
            high: 80–100

        Rules:
        - Return ONLY valid JSON.
        - Do NOT include any explanation, text, or markdown outside JSON.
        - Ensure the JSON is parseable.
        - If information is insufficient, still make a best-effort classification.
        - If budget is provided → weigh it heavily in scoring
        - If budget is missing → rely on intent and urgency

        Fallback (use ONLY if completely impossible to classify):
        {
            "intent": "unknown",
            "lead_score": 10,
            "category": "low",
            "confidence": 0.2,
            "reasoning": "Insufficient information to determine intent."
        }
        """
        
        user_prompt = f"Lead Name: {lead_name}\nLead Message: {lead_message}"
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        
        
        result_text = response.choices[0].message.content
        json_text = re.search(r'\{.*\}', result_text, re.DOTALL).group()
        result_dict = json.loads(json_text)
        
        log_event("ai_response_received", {"intent": result_dict.get("intent"), "score": result_dict.get("lead_score")})
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
