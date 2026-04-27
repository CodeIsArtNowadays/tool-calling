from pydantic import BaseModel


class AskRequestSchema(BaseModel):
    prompt: str
    
    
class AskResponseSchema(BaseModel):
    answer: str