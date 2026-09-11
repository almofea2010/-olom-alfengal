from pydantic import BaseModel, Field


class PostRequest(BaseModel):
    idea: str = Field(min_length=1, max_length=500)
    mood: str = Field(default="زوارة الخميس", max_length=80)
    cafe_name: str = Field(default="", max_length=120)
    tone: str = Field(default="حماسي", max_length=80)
    provider: str = Field(default="chatgpt", max_length=30)


class PostResult(BaseModel):
    text: str
    hashtags: list[str]
    call_to_action: str
    mode: str
