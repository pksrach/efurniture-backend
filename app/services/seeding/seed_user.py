# app/services/seeding/seed_user.py

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from app.config.security import hash_password
from app.constants.roles import Roles
from app.models.user import User


class SeedUser:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def user_exists(self, email: str, username: str) -> bool:
        stmt = select(User).filter(or_(User.email == email, User.username == username))
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def seed_users(self):
        if not await self.user_exists("admin@example.com", "admin"):
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password=hash_password("admin@123"),
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                role=Roles.ADMIN
            )
            self.session.add(admin_user)
        else:
            return "Users already seeded."

        if not await self.user_exists("superadmin@example.com", "superadmin"):
            super_admin_user = User(
                username="superadmin",
                email="superadmin@example.com",
                password=hash_password("superadmin@123"),
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                role=Roles.SUPER_ADMIN
            )
            self.session.add(super_admin_user)
        else:
            return "Users already seeded."

    async def run(self):
        async with self.session.begin():
            await self.seed_users()
        await self.session.commit()

        return "Users seeded successfully."
