from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func
from app.models.event import Event as EventModel


class EventsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_event(self, event: EventModel):
        place = event.place

        stmt = insert(EventModel).values(
            id=event.id,
            name=event.name,
            event_time=event.event_time,
            registration_deadline=event.registration_deadline,
            status=event.status,
            number_of_visitors=event.number_of_visitors,
            changed_at=event.changed_at,
            created_at=event.created_at,
            status_changed_at=event.status_changed_at,

            place_id=place.id,
            place_name=place.name,
            place_city=place.city,
            place_address=place.address,
            place_seats_pattern=place.seats_pattern,
            place_changed_at=place.changed_at,
            place_created_at=place.created_at,
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[EventModel.id],
            set_={
                "name": stmt.excluded.name,
                "event_time": stmt.excluded.event_time,
                "registration_deadline": stmt.excluded.registration_deadline,
                "status": stmt.excluded.status,
                "number_of_visitors": stmt.excluded.number_of_visitors,
                "changed_at": stmt.excluded.changed_at,
                "status_changed_at": stmt.excluded.status_changed_at,

                "place_id": stmt.excluded.place_id,
                "place_name": stmt.excluded.place_name,
                "place_city": stmt.excluded.place_city,
                "place_address": stmt.excluded.place_address,
                "place_seats_pattern": stmt.excluded.place_seats_pattern,
                "place_changed_at": stmt.excluded.place_changed_at,
                "place_created_at": stmt.excluded.place_created_at,
            }
        )

        await self.session.execute(stmt)
        await self.session.commit()
        
    async def get_events(self, date_from, limit, offset):
        stmt = select(EventModel)

        if date_from:
            stmt = stmt.where(EventModel.event_time >= date_from)

        stmt = stmt.order_by(EventModel.event_time.asc())
        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_event_by_id(self, event_id: str):
        stmt = select(EventModel).where(EventModel.id == event_id)
        result = await self.session.execute(stmt)
        event = result.scalar_one_or_none()
        return event
    
    async def count_events(self, date_from):
        stmt = select(func.count(EventModel.id))

        if date_from:
            stmt = stmt.where(EventModel.event_time >= date_from)

        result = await self.session.execute(stmt)
        return result.scalar()