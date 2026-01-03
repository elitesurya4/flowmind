from pydantic import BaseModel
from typing import List, Optional

class ChatTurn(BaseModel):
    role: str
    content: str

class ValidationStep(BaseModel):
    step_no: int
    action: str
    expected_result: str
    category: str

class ValidationPlan(BaseModel):
    system_name: str
    validation_type: str
    steps: List[ValidationStep]

class AgentState(BaseModel):
    session_id: str
    user_query: str
    chat_history: List[ChatTurn] = []
    retrieved_context: Optional[str] = None
    plan: Optional[ValidationPlan] = None
    confidence: Optional[float] = None