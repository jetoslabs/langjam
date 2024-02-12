import json
from enum import Enum
from typing import Optional

import pytest
from pydantic import BaseModel, Field

from src.langjam.openai_utils import get_openai_function_defination
from tests.chat_req import ChatReq
from tests.expected import get_current_weather_expected


class Unit(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"


class GetCurrentWeatherParams(BaseModel):
    location: str = Field(description="The city and state, e.g. San Francisco, CA")
    # unit: Unit
    unit: Optional[Unit] = None
    # unit: None | Unit = None


async def get_current_weather(get_current_weather_params: GetCurrentWeatherParams):
    return "ok"


@pytest.mark.asyncio
async def test_func_to_tool_happy_path_1():
    func = get_current_weather
    resp = await get_openai_function_defination(func, "Get the current weather in a given location")
    assert (
            resp.model_dump_json(exclude_none=True).replace(" ", "") ==
            json.dumps(get_current_weather_expected).replace(" ", "")
    )


async def get_chat_req_test(chat_req: ChatReq):
    return "get_chat_req_test"


@pytest.mark.asyncio
async def test_func_to_tool_happy_path_2():
    func = get_chat_req_test
    mjs = ChatReq.model_json_schema()
    resp = await get_openai_function_defination(func, "Get the Openai chat")
    assert (
            resp.model_dump_json(exclude_none=True).replace(" ", "") ==
            json.dumps(get_current_weather_expected).replace(" ", "")
    )
