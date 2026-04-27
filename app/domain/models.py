from typing import Any

from pydantic import BaseModel, Field


class StudyUploadResponse(BaseModel):
    study_id: str
    status: str
    enqueue_processing: bool
    job_id: str | None = None


class JobCreateRequest(BaseModel):
    study_id: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class JobCreateResponse(BaseModel):
    job_id: str
    study_id: str
    status: str


class JobStateResponse(BaseModel):
    job_id: str
    study_id: str
    status: str
    created_at: str
    updated_at: str
    source: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    queue: dict[str, Any] = Field(default_factory=dict)
    result: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class JobResultResponse(BaseModel):
    job_id: str
    study_id: str
    result: dict[str, Any]
