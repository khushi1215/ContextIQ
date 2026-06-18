from backend import database


class LoggingService:
    def log_interaction(
        self,
        question: str,
        answer: str,
        latency_ms: float,
        answer_found: bool,
    ) -> int:
        return database.insert_query_log(
            question=question,
            answer=answer,
            latency_ms=latency_ms,
            answer_found=answer_found,
        )
