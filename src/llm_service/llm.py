import json

from openai import OpenAI

from config import settings
from src.llm_service import tools


class LLMService:

    def __init__(self):
        self.client = OpenAI( base_url="https://openrouter.ai/api/v1", api_key=settings.api_key)
        self.model = settings.ai_model
        
        self.TOOLS = {
            'get_from_table': {
                'function': tools.get_from_table,
                'schema': {
                    'type': 'function',
                    'function': {
                        'name': 'get_from_table',
                        'description': 'Get rows from database table filtered by time period',
                        'parameters': {
                            'type': 'object',
                            'properties': {
                                'table': {
                                    'type': 'string',
                                    'description': 'Table name to query'
                                },
                                'time': {
                                    'type': 'integer',
                                    'description': 'Time period in hours to filter by. Defaults to 1 hour, if not provide'
                                    # 'properties': {
                                    #     'hours': {'type': int, 'description': 'Number of hours'},
                                    #     'minutes': {'type': int, 'description': 'Number of minutes'},
                                    #     'days': {'type': int, 'description': 'Number of days'},
                                    # },
                                    # 'additionalProperties': False
                                }
                            },
                            'required': ['table'],
                            'additionalProperties': False
                        }
                    }
                }
            },
            'restart_service': {
                'function': tools.restart_service,
                'schema': {
                    'type': 'function',
                    'function': {
                        'name': 'restart_service',
                        'description': 'Stop and start given service, logging given reason if provided',
                        'parameters': {
                            'type': 'object',
                            'properties': {
                                'service': {
                                    'type': 'string',
                                    'description': 'Name of service to restart'
                                },
                                'reason': {
                                    'type': 'string',
                                    'description': 'Reason of why service needs to be restarted. Using for logs only'
                                }
                            },
                            'required': ['service'],
                            'additionalProperties': False
                        }
                    }
                }
            },
            'get_service_status': {
                'function': tools.get_service_status,
                'schema': {
                    'type': 'function',
                    'function': {
                        'name': 'get_service_status',
                        'description': 'Get current service status (running, stopped, error)',
                        'parameters': {
                            'type': 'object',
                            'properties': {
                                'service': {
                                    'type': 'string',
                                    'description': 'Name of service to get status'
                                }
                            },
                            'required': ['service'],
                            'additionalProperties': False
                        }
                    }
                } 
            }
        }
        
        
        
    def get_response_from_llm(self, messages):
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=[t['schema'] for t in self.TOOLS.values()],
            tool_choice='auto'
        )
        
        return response
        
    def ask_llm(self, prompt):
        messages = []
        messages.append({'role': 'user', 'content': prompt})
        
        while True:
        
            response = self.get_response_from_llm(messages)
            
            message = response.choices[0].message
                
            messages.append(message)
            finish_reason = response.choices[0].finish_reason
            
            if finish_reason == 'stop':
                break 
            elif finish_reason == 'tool_calls':
                for tool in message.tool_calls: # type: ignore
                    
                    func = self.TOOLS[tool.function.name]['function'] # type: ignore
                    args = json.loads(tool.function.arguments) # type: ignore
                    result = func(**args)
                    
                    messages.append({
                        'role': 'tool',
                        'tool_call_id': tool.id,
                        'content': json.dumps(result)
                    })
        print(messages)
        return message.content
                    
        
        
    
    
llm_service = LLMService()