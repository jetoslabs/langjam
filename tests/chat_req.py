from typing import List, Literal, Optional, Dict, Union

import httpx
from openai._types import Headers, Query, Body
from openai.types.chat import ChatCompletionMessageParam, completion_create_params, ChatCompletionToolChoiceOptionParam, \
    ChatCompletionToolParam
from pydantic import BaseModel, ConfigDict


class ChatReq(BaseModel):
    messages: List[ChatCompletionMessageParam]
    model: Literal[
        "gpt-4-1106-preview",
        "gpt-4-vision-preview",
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-0613",
        "gpt-4-32k",
        "gpt-4-32k-0314",
        "gpt-4-32k-0613",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo-16k-0613",
        ] = "gpt-3.5-turbo-16k-0613"
    frequency_penalty: Optional[float] = None
    # function_call: completion_create_params.FunctionCall = None
    # functions: List[completion_create_params.Function] = None
    logit_bias: Optional[Dict[str, int]] = None
    logprobs: Optional[bool] = None
    max_tokens: Optional[int] = 2000
    n: Optional[int] = 1
    presence_penalty: Optional[float] = None
    response_format: Optional[completion_create_params.ResponseFormat] = None
    seed: Optional[int] = None
    stop: Union[Optional[str], List[str]] = "stop"
    stream: Optional[Literal[False]] | Literal[True] = False
    temperature: Optional[float] = 0.8
    tool_choice: ChatCompletionToolChoiceOptionParam | None = None
    tools: List[ChatCompletionToolParam] | None = None
    top_logprobs: Optional[int] = None
    top_p: Optional[float] = None
    user: str | None = None
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Headers | None = None
    extra_query: Query | None = None
    extra_body: Body | None = None
    timeout: float | httpx.Timeout | None = 180

    model_config = ConfigDict(arbitrary_types_allowed=True)
