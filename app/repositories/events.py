from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.models.event import Event


class EventsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_event(self, event: dict):
        place = event["place"]

        stmt = insert(Event).values(
            id=event["id"],
            name=event["name"],
            event_time=event["event_time"],
            registration_deadline=event["registration_deadline"],
            status=event["status"],
            number_of_visitors=event["number_of_visitors"],
            changed_at=event["changed_at"],
            created_at=event["created_at"],
            status_changed_at=event["status_changed_at"],

            place_id=place["id"],
            place_name=place["name"],
            place_city=place["city"],
            place_address=place["address"],
            place_seats_pattern=place["seats_pattern"],
            place_changed_at=place["changed_at"],
            place_created_at=place["created_at"],
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[Event.id],
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