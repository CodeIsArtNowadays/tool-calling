from fastapi import APIRouter, HTTPException

from src.api.schemas import AskRequestSchema, AskResponseSchema
from src.llm_service.llm import llm_service

api_router = APIRouter()


@api_router.get("/")
async def index():
    return {"status": "ok"}


@api_router.post("/llm", response_model=AskResponseSchema)
async def llm(request: AskRequestSchema):
    try:
        result = await llm_service.ask_llm(request.prompt)
        return {'answer': result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
