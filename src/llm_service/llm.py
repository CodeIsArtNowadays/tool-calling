from openai import AsyncOpenAI

from config import settings
from src.llm_service import tools
from src.llm_service.schemas import Tool, GetFromTableToolSchema, GetServiceStatusToolSchema, RestartServiceToolSchema
from src.core.sessions import session_manager


class LLMService:

    def __init__(self):
        self.client = AsyncOpenAI( base_url="https://openrouter.ai/api/v1", api_key=settings.api_key)
        self.model = settings.ai_model
        
        self.TOOLS = {
            'get_from_table': Tool(
                name='get_from_table',
                description='Get rows from database table filtered by time period',
                arg_schema=GetFromTableToolSchema,
                function=tools.get_from_table
            ),
            'restart_service': Tool(
                name='restart_service',
                description='Stop and start given service, logging given reason if provided',
                arg_schema=RestartServiceToolSchema,
                function=tools.restart_service
            ),
            'get_service_status': Tool(
                name='get_service_status',
                description='Get current service status (running, stopped, error)',
                arg_schema=GetServiceStatusToolSchema,
                function=tools.get_service_status
            ),
        }
        
    async def get_response_from_llm(self, messages):
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=[t.to_openai_schema() for t in self.TOOLS.values()], # type: ignore
            tool_choice='auto'
        )
        
        return response
        
    async def ask_llm(self, prompt: str, session_id: str):
        messages = session_manager.get_or_create(session_id)
        
        if not messages:
            messages.append({
                'role': 'system',
                'content': '''You are DevOps assistant. 
                When asked about past actions, look through the conversation history and tool call results — the answer is already there.
                Do not say you lack access if the information is visible in the chat history.'''
            })

        messages.append({'role': 'user', 'content': prompt})
        
        while True:
        
            response = await self.get_response_from_llm(messages)
            
            message = response.choices[0].message
                
            messages.append(message.model_dump(exclude_none=True))
            finish_reason = response.choices[0].finish_reason
            
            if finish_reason == 'stop':
                break 
            elif finish_reason == 'tool_calls':
                for tool in message.tool_calls: # type: ignore
                    
                    result = self.TOOLS[tool.function.name].run(tool.function.arguments) # type: ignore
                    
                    messages.append({
                        'role': 'tool',
                        'tool_call_id': tool.id,
                        'content': result
                    })
        print(messages)
        
        return message.content
                    
        
        
    
    
llm_service = LLMService()