import json

import pytest
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
from pydantic import BaseModel, Field

from src.langjam.openai.openai_function.openai_function import OpenaiFunction
from tests.openai.openai_function.test_openai_function import get_current_weather, GetCurrentWeatherParams
from tests.openai.openai_function.web_search import Search

OPENAI_ORG_ID=""
OPENAI_API_KEY=""


class GetWebSearch(BaseModel):
    text: str = Field(description="Text to do websearch on")


async def get_current_weather(get_current_weather_params: GetCurrentWeatherParams):
    return "30"


@pytest.mark.asyncio
async def test_openai_with_function_happy_path_1():
    client = AsyncOpenAI(api_key=OPENAI_API_KEY,organization=OPENAI_ORG_ID,timeout=180)
    message1 = ChatCompletionSystemMessageParam(content="You are helpful assistant", role="system")
    message2 = ChatCompletionUserMessageParam(role="user", content="Should I wear heavy jacket or light jacket while going out in in Boston today?")
    # message2 = ChatCompletionUserMessageParam(role="user", content="What is the latest news in India?")

    func_obj_2 = await OpenaiFunction.get_defination(Search().search_text, "Search text on web")

    func_obj_1 = await OpenaiFunction.get_defination(get_current_weather, "Get the current weather in a given location")

    tools = [func_obj_1, func_obj_2]
    messages = [message1,message2]

    is_done = False
    try:
        while not is_done:
            chat_completion = await client.chat.completions.create(messages=messages, model="gpt-4", tools=tools)
            finish_reason = chat_completion.choices[-1].finish_reason
            match finish_reason:
                case "tool_calls":
                    f = chat_completion.choices[-1].message.tool_calls[-1].function
                    match f.name:
                        case 'get_current_weather':
                            args_dict = json.loads(f.arguments)
                            params = GetCurrentWeatherParams(**args_dict)
                            res = await get_current_weather(params)
                            messages.append(ChatCompletionUserMessageParam(role="user", content=f"get_current_weather result: {res} degree Fahrenheit"))
                case "content_filter":
                    message = ChatCompletionUserMessageParam(role="user", content="Create output the is safe for content filter")
                    messages.append(message)
                case "stop":
                    content = chat_completion.choices[-1].message.content
                    message = ChatCompletionUserMessageParam(role="user", content=content)
                    messages.append(message)
                    is_done = True
                case _:
                    is_done = True

            assert chat_completion
    except Exception as e:
        print(str(e))
