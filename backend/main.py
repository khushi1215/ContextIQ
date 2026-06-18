from fastapi import FastAPI

from backend.config import settings
from backend.database.init_db import init_db
from backend.routers import ask, ingest, analytics
from backend.schemas import HealthResponse

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="Scaffold for a RAG-based Document Q&A System.",
)

app.include_router(ask.router)
app.include_router(ingest.router)
app.include_router(analytics.router)


@app.on_event("startup")
async def on_startup() -> None:
    init_db()    #Initialize database


@app.get("/health", response_model=HealthResponse, summary="Health check")
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=settings.APP_VERSION)    #HealthCheck
