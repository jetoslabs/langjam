from enum import Enum
from typing import Literal, List

from openai import BaseModel
from pydantic import Field, field_validator

from tests.openai.openai_function.web_search_region_model import Region


class Timelimit(str, Enum):
    all = "all"
    d = "day"
    w = "week"
    m = "month"
    y = "year"


class SearchTextParams(BaseModel):
    keywords: str
    region: Region = Region.wt_wt
    safesearch: Literal["on", "moderate", "off"] = "moderate"
    timelimit: Timelimit | None = None
    max_results: int = Field(3, ge=1, le=10)

    @field_validator("region", "timelimit")
    @classmethod
    def get_enum_name(cls, value):
        if isinstance(value, Enum):
            if isinstance(value, Timelimit):
                if value == Timelimit.all:
                    return None
            return value.name
        return value


class SearchTextParams1(BaseModel):
    keywords1: str
    region1: Region = Region.wt_wt
    safesearch1: Literal["on", "moderate", "off"] = "moderate"
    timelimit1: Timelimit | None = None
    max_results1: int = Field(3, ge=1, le=10)

    @field_validator("region1", "timelimit1")
    @classmethod
    def get_enum_name(cls, value):
        if isinstance(value, Enum):
            if isinstance(value, Timelimit):
                if value == Timelimit.all:
                    return None
            return value.name
        return value


class SearchRes(BaseModel):
    title: str
    href: str
    body: str


class Search:
    # async def search_text(self, search_params: SearchTextParams, params1: SearchTextParams1) -> List[SearchRes]:
    async def search_text(self, search_params: SearchTextParams) -> List[SearchRes]:
        search_res = []
        s = SearchRes(title="title", href="href", body="body")
        return search_res
