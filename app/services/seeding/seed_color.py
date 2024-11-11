from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.color import Color


class SeedColor:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def color_exists(self, name: str) -> bool:
        stmt = select(Color).filter(Color.name == name)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def seed_color(self):
        colors = [
            {"code": "Red", "name": "Red", "highlight": "Red"},
            {"code": "Blue", "name": "Blue", "highlight": "Blue"},
            {"code": "Green", "name": "Green", "highlight": "Green"},
            {"code": "Yellow", "name": "Yellow", "highlight": "Yellow"},
            {"code": "Orange", "name": "Orange", "highlight": "Orange"},
            {"code": "Purple", "name": "Purple", "highlight": "Purple"},
            {"code": "Black", "name": "Black", "highlight": "Black"},
            {"code": "White", "name": "White", "highlight": "White"},
            {"code": "Pink", "name": "Pink", "highlight": "Pink"},
            {"code": "Brown", "name": "Brown", "highlight": "Brown"}
        ]

        for color in colors:
            if not await self.color_exists(color["name"]):
                new_color = Color(
                    code=color["code"],
                    name=color["name"],
                    highlight=color["highlight"]
                )
                self.session.add(new_color)
            else:
                return "Colors already seeded."

    async def run(self):
        async with self.session.begin():
            await self.seed_color()
        await self.session.commit()

        return "Colors seeded successfully"
