from fastapi import APIRouter

from backend.schemas import AskRequest, AskResponse
from backend.services.rag_service import RagService
from backend.services.logging_service import LoggingService

router = APIRouter()

_rag = RagService()
_logger = LoggingService()

NO_ANSWER = "The requested information is not available in the provided document."


@router.post(
    "/ask",
    response_model=AskResponse,
    summary="Answer a question",
)
def ask(request: AskRequest) -> AskResponse:
    response = _rag.ask_question(request.query)

    # Persist interaction for analytics.
    answer_found = (
    "not available in the provided document"
    not in response.answer.lower())
    _logger.log_interaction(
        question=request.query,
        answer=response.answer,
        latency_ms=response.latency_ms,
        answer_found=answer_found,
        )

    return response