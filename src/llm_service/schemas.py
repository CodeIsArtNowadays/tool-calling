import json
from typing import Callable
from dataclasses import dataclass

from pydantic import BaseModel, Field, ValidationError


@dataclass
class Tool:
    name: str
    description: str
    arg_schema: type[BaseModel]
    function: Callable
    
    def to_openai_schema(self) -> dict:
        raw_schema = self.arg_schema.model_json_schema()
        
        for prop in raw_schema['properties'].values():
            prop.pop('title', None)
            
        return {
            'type': 'function',
            'function': {
                'name': self.name,
                'description': self.description,
                'parameters': {
                    'type': 'object',
                    'properties': raw_schema['properties'],
                    'required': raw_schema.get('required', []),
                    'additionalProperties': False
                }
            }
        }
    
    
    def run(self, raw_args: str) -> str:
        try:
            kwargs = self.arg_schema(**json.loads(raw_args)).model_dump()
            return json.dumps(self.function(**kwargs))
        except ValidationError:
            return 'Invalid arguments' + str(raw_args)

class GetFromTableToolSchema(BaseModel):
    table: str = Field(description='Table name to query')
    time: int = Field(default=1, description='Time period in hours to filter by. Defaults to 1 hour, if not provide')
    
    
class GetServiceStatusToolSchema(BaseModel):
    service: str = Field(description='Name of service to get status')
    

class RestartServiceToolSchema(BaseModel):
    service: str = Field(description='Name of service to restart')
    reason: str | None = Field(default=None, description='Reason of why service needs to be restarted. Using for logs only')