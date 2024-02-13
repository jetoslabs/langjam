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

    class ConfigDict:
        exclude_none = True
