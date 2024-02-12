from typing import Optional, List, Dict

from pydantic import BaseModel


class PropertyObj(BaseModel):
    type: str
    description: Optional[str] = None
    enum: List[str] | None = None


class ParametersObj(BaseModel):
    type: str = "object"
    properties: Dict[str, PropertyObj]
    required: List[str]


class FunctionObj(BaseModel):
    name: str
    description: str
    parameters: ParametersObj


class FunctionSchema(BaseModel):
    type: str = "function"
    function: FunctionObj

    class Config:
        exclude_none = True


get_current_weather_expected = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    }
}
