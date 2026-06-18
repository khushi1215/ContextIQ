from backend import database


class AnalyticsService:
    def get_total_queries(self) -> int:
        return database.get_total_queries()    #Total logged question

    def get_average_latency(self) -> float:
        return database.get_average_latency()     #Avg response latency

    def get_unanswered_queries(self) -> int:
        return database.get_unanswered_queries()     #Total unanswered questions

    def get_most_frequent_questions(
        self,
        limit: int = 5,
    ) -> list[dict]:
        return database.get_frequent_questions(limit)    #FAQs