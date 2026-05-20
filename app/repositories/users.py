from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: dict) -> User:
        user_instance = User(
            id=str(uuid4()),
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
        )
        self.session.add(user_instance)
        await self.session.commit()
        return user_instance

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
