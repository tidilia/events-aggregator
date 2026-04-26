from sqlalchemy import Column, String, DateTime
from app.db.base import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))