from sqlalchemy import Column, Integer, DateTime, String
from app.db.base import Base


class SyncMetadata(Base):
    __tablename__ = "sync_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)

    last_sync_time = Column(DateTime, nullable=False)
    last_changed_at = Column(DateTime, nullable=False)

    sync_status = Column(String, nullable=False)