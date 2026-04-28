from pydantic import BaseModel


class AskRequestSchema(BaseModel):
    prompt: str
    session_id: str | None = None
    
    
class AskResponseSchema(BaseModel):
    answer: str
    session_id: str