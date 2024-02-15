import json
from enum import Enum
from typing import Optional

import pytest
from pydantic import BaseModel, Field

from src.langjam.openai.openai_function.openai_function import OpenaiFunction
from tests.openai.openai_function.expected import get_current_weather_expected


class Unit(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"


class GetCurrentWeatherParams(BaseModel):
    location: str = Field(description="The city and state, e.g. San Francisco, CA")
    # unit: Unit
    unit: Optional[Unit] = None
    # unit: None | Unit = None


async def get_current_weather(get_current_weather_params: GetCurrentWeatherParams):
    return "30"


@pytest.mark.asyncio
async def test_get_definition_happy_path_1():
    func = get_current_weather
    resp = await OpenaiFunction.get_defination(
        func, "Get the current weather in a given location"
    )
    assert (
            json.dumps(resp).replace(" ", "") ==
            json.dumps(get_current_weather_expected).replace(" ", "")
    )
