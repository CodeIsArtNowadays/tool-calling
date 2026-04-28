import uuid
from fastapi import APIRouter, HTTPException

from src.api.schemas import AskRequestSchema, AskResponseSchema
from src.llm_service.llm import llm_service

api_router = APIRouter()


@api_router.get("/")
async def index():
    return {"status": "ok"}


@api_router.post("/llm", response_model=AskResponseSchema)
async def llm(request: AskRequestSchema):
    
    if not request.session_id:
        request.session_id = str(uuid.uuid4())
    
    try:
        result = await llm_service.ask_llm(request.prompt, request.session_id)
        return {'session_id': request.session_id, 'answer': result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
