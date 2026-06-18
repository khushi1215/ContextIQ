from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""


class QueryLog(Base):
    __tablename__ = "query_logs"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    question: str = Column(Text, nullable=False)
    answer: str = Column(Text, nullable=False)
    timestamp: datetime = Column(DateTime, nullable=False, default=datetime.utcnow)
    latency_ms: float = Column(Float, nullable=False)
    answer_found: bool = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<QueryLog id={self.id} answer_found={self.answer_found} "
            f"latency_ms={self.latency_ms:.1f}>"
        )
