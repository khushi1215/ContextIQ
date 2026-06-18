from fastapi import APIRouter

from backend.schemas import AnalyticsResponse
from backend.services.analytics_service import AnalyticsService

router = APIRouter()
_analytics = AnalyticsService()


@router.get("/analytics", response_model=AnalyticsResponse, summary="Query log analytics")
def analytics() -> AnalyticsResponse:
    return AnalyticsResponse(
        total_queries=_analytics.get_total_queries(),
        average_latency_ms=round(_analytics.get_average_latency(), 2),
        unanswered_queries=_analytics.get_unanswered_queries(),
        most_frequent_questions=_analytics.get_most_frequent_questions(),
    )
