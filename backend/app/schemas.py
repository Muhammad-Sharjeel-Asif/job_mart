from datetime import UTC, date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class JobType(str, Enum):
    Fulltime = "Fulltime"
    Parttime = "Parttime"
    Hybrid = "Hybrid"
    Onsite = "Onsite"
    Remote = "Remote"


class JobBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=500)
    location: str = Field(min_length=3, max_length=50)
    job_type: JobType = Field(default=JobType.Fulltime)
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    deadline: date | None = Field(default=None)
    skills: list[str] = Field(default_factory=list)


class JobResponse(JobBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class JobCreate(JobBase):
    pass


# the input and output models should be different because of difference of fields. For input, you don't take some of the fields like id and created_at because of security reasons. And for output you may display them.


class JobUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, min_length=3, max_length=500)
    location: str | None = Field(default=None, min_length=3, max_length=50)
    job_type: JobType | None = None
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = None
    deadline: date | None = None
    skills: list[str] | None = None
