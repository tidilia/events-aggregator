from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from app.db.base import Base
from datetime import datetime, timezone

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    seat = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    __table_args__ = (
        UniqueConstraint("event_id", "seat", name="uq_event_seat"),
    )