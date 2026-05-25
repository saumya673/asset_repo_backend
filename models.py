from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID,uuid4

class Stats(BaseModel):
    label: str = Field(description="")
    value: str = Field(description="")
    sub: str = Field(description="")
    variant: Literal["gold","crimson","neutral"] = Field(description="neutral")
    progress: int = Field(default=0, description="")

class Project(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(description="")
    desc: str = Field(description="")
    rating: int = Field(description="", ge=1, le=5)
    badge: str = Field(description="")
    badge_variant: Literal["gold","crimson","neutral"] = Field(description="neutral")
    image: str = Field(description="")
    avatar_count: int = Field(default=0, description="")
    long_desc: str = Field(description="")
    tags: list[str]= Field(description="")
    service: str = Field(description="")
    domain: str = Field(description="")
    scope: str = Field(description="")
    type: str = Field(description="")
    stats: list[Stats] = Field(description="")
