from fastapi import APIRouter

from src.llm_service.llm import llm_service


api_router = APIRouter()


@api_router.get('/')
async def index():
    return {'status': 'ok'}
    
    
@api_router.get('/llm')
async def llm():
    
    return llm_service.ask_llm("check status of nginx and postgres")