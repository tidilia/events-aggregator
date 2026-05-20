from sqlalchemy import JSON, Column, DateTime, ForeignKey, String

from app.db.base import Base


class Outbox(Base):
    __tablename__ = "outbox"

    id = Column(String, primary_key=True)
    payload = Column(JSON, nullable=False)
    ticket_id = Column(String, ForeignKey("tickets.id"), nullable=False)

    status = Column(String, default="pending")  # pending/sent
    created_at = Column(DateTime(timezone=True))
