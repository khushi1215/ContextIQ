from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The question to answer.")


class AskResponse(BaseModel):
    answer: str = Field(..., description="The generated answer.")
    sources: list[str] = Field(..., description="Source document references.")
    latency_ms: float = Field(..., description="Time taken to generate the answer in milliseconds.")


class IngestResponse(BaseModel):
    message: str = Field(..., description="Status message describing the ingest result.")


class AnalyticsResponse(BaseModel):
    total_queries: int = Field(..., description="Total number of queries logged.")
    average_latency_ms: float = Field(..., description="Average response latency in milliseconds.")
    unanswered_queries: int = Field(..., description="Number of queries with no answer found.")
    most_frequent_questions: list = Field(..., description="Most commonly asked questions.")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status.")
    version: str = Field(..., description="API version string.")
