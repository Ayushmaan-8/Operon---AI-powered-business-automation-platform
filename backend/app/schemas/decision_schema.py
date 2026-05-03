from pydantic import BaseModel

class AIDecisionResponse(BaseModel):
    intent: str
    lead_score: int
    category: str
    confidence: float
    reasoning: str
