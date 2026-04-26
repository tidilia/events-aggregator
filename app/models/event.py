from sqlalchemy import Column, String, DateTime, Integer
from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)

    name = Column(String, nullable=False)
    event_time = Column(DateTime(timezone=True), nullable=False)
    registration_deadline = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False)
    number_of_visitors = Column(Integer, nullable=False)

    changed_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    status_changed_at = Column(DateTime(timezone=True), nullable=False)

    # place (денормализовано)
    place_id = Column(String)
    place_name = Column(String)
    place_city = Column(String)
    place_address = Column(String)
    place_seats_pattern = Column(String)
    place_changed_at = Column(DateTime(timezone=True))
    place_created_at = Column(DateTime(timezone=True))