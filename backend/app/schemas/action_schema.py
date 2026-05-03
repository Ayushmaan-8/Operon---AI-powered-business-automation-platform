from pydantic import BaseModel

class ActionResponse(BaseModel):
    action: str
    priority: str
    reason: str
