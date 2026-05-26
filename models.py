from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID,uuid4

from categories import Domain, ProjectType, Scope, Service

AllowedTag = Service | Domain | Scope | ProjectType

class Stats(BaseModel):
    label: str = Field(default="", description="")
    value: str = Field(default="", description="")
    sub: str = Field(default="", description="")
    variant: Literal["gold","crimson","neutral"] = Field(default="neutral", description="neutral")
    progress: int = Field(default=0, description="")

class Project(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(description="Title of the ppt")
    desc: str = Field(default="", description="")
    rating: int = Field(description="", ge=1, le=5)
    badge: str = Field(default="", description="")
    badge_variant: Literal["gold","crimson","neutral"] = Field(default="neutral", description="neutral")
    image: str = Field(default="", description="Image url")
    avatar_count: int = Field(default=0, description="")
    long_desc: str = Field(default="", description="")
    tags: list[AllowedTag] = Field(
        default_factory=list,
        description="Zero or more tags selected only from the allowed service, domain, scope, and type values."
    )
    service: Service = Field(description="One allowed service value.")
    domain: Domain = Field(description="One allowed domain value.")
    scope: Scope = Field(description="One allowed scope value.")
    isu: str = Field(default="", description="Business domain name like Banking, Financial Services & Insurance (BFSI); Healthcare; Retail")
    sub_Isu: str = Field(default="", description="Sub business domain name")
    account: str = Field(default="", description="")
    type: ProjectType = Field(description="One allowed type value.")
    implemented_year: str = Field(default="", description="year in which this project was build")
    associate_name: str = Field(default="", description="person who build or took lead in this project")
    associate_role: str = Field(default="", description="role of the person in the project")
    stats: list[Stats] = Field(default_factory=list, description="")
