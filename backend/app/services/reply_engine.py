import re
from groq import Groq
from app.core.config import settings
from app.utils.monitoring import log_event, log_error


def generate_reply(lead_name: str, lead_message: str, intent: str, category: str) -> str:
    log_event("reply_generation_start", {
        "lead_name": lead_name,
        "category": category
    })

    if not settings.GROQ_API_KEY:
        return fallback_reply(lead_name, category)

    try:
        client = Groq(api_key=settings.GROQ_API_KEY)

        system_prompt = """
        You are a sales assistant for a business automation company.

        Your job is to generate a short, natural, human-like reply to a lead.

        Tone:
        - Professional
        - Friendly
        - Not robotic
        - Not too long (2–4 lines max)

        Behavior:
        - HIGH priority → push for immediate call/action
        - MEDIUM → encourage discussion
        - LOW → ask for more details

        Do NOT sound like AI.
        Do NOT include placeholders like [Name].
        """

        user_prompt = f"""
        Lead Name: {lead_name}
        Message: {lead_message}
        Intent: {intent}
        Priority: {category}

        Generate reply only.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()

        log_event("reply_generated", {"category": category})

        return reply

    except Exception as e:
        log_error("reply_error", {"error": str(e)})
        return fallback_reply(lead_name, category)


def fallback_reply(lead_name: str, category: str) -> str:
    if category == "high":
        return f"Hi {lead_name}, thanks for reaching out. We can prioritize this immediately — when can we connect?"
    elif category == "medium":
        return f"Hi {lead_name}, thanks for your message. Let’s discuss your automation needs in more detail."
    else:
        return f"Hi {lead_name}, thanks for reaching out. Could you share a bit more about what you're looking for?"