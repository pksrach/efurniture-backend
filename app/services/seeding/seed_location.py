from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Location


class SeedLocation:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def location_exists(self, name: str) -> bool:
        stmt = select(Location).filter(Location.name == name)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def seed_location(self):
        locations = [
            {"name": "Phnom Penh", "price": 1.00, "parent_id": None},
            {"name": "Siem Reap", "price": 2.00, "parent_id": None},
            {"name": "Battambang", "price": 3.00, "parent_id": None},
            {"name": "Sihanoukville", "price": 4.00, "parent_id": None},
            {"name": "Kampot", "price": 5.00, "parent_id": None},
            {"name": "Kandal", "price": 6.00, "parent_id": None},
            {"name": "Koh Kong", "price": 7.00, "parent_id": None},
            {"name": "Kampong Cham", "price": 8.00, "parent_id": None},
            {"name": "Kampong Chhnang", "price": 1.00, "parent_id": None},
            {"name": "Kampong Speu", "price": 2.00, "parent_id": None},
            {"name": "Kampong Thom", "price": 3.00, "parent_id": None},
            {"name": "Kep", "price": 4.00, "parent_id": None},
            {"name": "Kratie", "price": 5.00, "parent_id": None},
            {"name": "Mondulkiri", "price": 6.00, "parent_id": None},
            {"name": "Oddar Meanchey", "price": 7.00, "parent_id": None},
            {"name": "Pailin", "price": 8.00, "parent_id": None},
            {"name": "Preah Vihear", "price": 1.00, "parent_id": None},
            {"name": "Prey Veng", "price": 2.00, "parent_id": None},
            {"name": "Pursat", "price": 3.00, "parent_id": None},
            {"name": "Ratanakiri", "price": 4.00, "parent_id": None},
            {"name": "Stung Treng", "price": 5.00, "parent_id": None},
            {"name": "Svay Rieng", "price": 6.00, "parent_id": None},
            {"name": "Takeo", "price": 7.00, "parent_id": None},
            {"name": "Tboung Khmum", "price": 8.00, "parent_id": None},
            {"name": "Banteay Meanchey", "price": 1.00, "parent_id": None},
        ]

        for location in locations:
            if not await self.location_exists(location["name"]):
                new_location = Location(
                    name=location["name"],
                    price=location["price"],
                    parent_id=location["parent_id"]
                )
                self.session.add(new_location)
            else:
                return "Locations already seeded."

    async def run(self):
        async with self.session.begin():
            await self.seed_location()
        await self.session.commit()

        return "Locations seeded successfully"
