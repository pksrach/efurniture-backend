from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.brand import Brand


class SeedBrand:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def brand_exists(self, name: str) -> bool:
        stmt = select(Brand).filter(Brand.name == name)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def seed_brand(self):
        brands = [
            {"name": "IKEA",
             "attachment": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQT1EAjxILR9h_uomrwzUls7EL2UvhUTbMbsY3QQeTouksujR1H_r1ZUVRECltM"},
            {"name": "Restoration Hardware",
             "attachment": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNRMbQlaI9aD9RSzzSYyLLIS51zgzx88gI0YZFJjK6cRzaK5GS06X3CyUD6U6P"},
            {"name": "West Elm",
             "attachment": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQ8LAf7bQ0HHdqu7-xNRcO-OXV9gzBWBrANdu48twP5x07uGlpSmXlrLH3J1YKr"},
            {"name": "Ethan Allen",
             "attachment": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTWJZQs2dNWJtUCqvQJYtScOqOjYqZOU9nxCrye2Xvkt8vO_br8ZOIPvvV84VCO"},
            {"name": "Ashley Furniture",
             "attachment": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQdAKC3HYzlcH5Iw_sjuNG9PAecGEYEZIezLR1q6_0q2ibkrwB5ks9mytOq-t2o"},
            {"name": "La-Z-Boy",
             "attachment": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcRu8ZulVh5GEepZczZL0P4pX09JyiQdLorFDqfbehjrOlzQVdOgf4q05SFHyco3"},
            {"name": "Room & Board",
             "attachment": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRop0IleTm_rxJ2ZEpvX1UWUqDVf_N3ORwobFo4-RFbcb6n2H8Nu5aUfda9jc5e"},
            {"name": "CB2",
             "attachment": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4aAgwalCnIJBQZOIU7B6f2zTVrQQDj9jRGMXwpkTaIZNIsY5yrefolJjhRJps"},
            {"name": "Flexsteel",
             "attachment": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcT3DbaJnCMLrBsaIxEsUFIpNoKZ6IKkzwzO4uATEFDp9zjIo4gQJYow9Uc-kQe3"},
            {"name": "Havertys",
             "attachment": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQztEnYtSfuCBLJqTLYaSePOUhq8n41mSYE2ZM_Ee9JXfJRjEc72lCJOyo6BYtG"},
        ]

        for brand in brands:
            if not await self.brand_exists(brand["name"]):
                new_brand = Brand(
                    name=brand["name"],
                    attachment=brand["attachment"]
                )
                self.session.add(new_brand)
            else:
                return "Categories already seeded."

    async def run(self):
        async with self.session.begin():
            await self.seed_brand()
        await self.session.commit()

        return "Brands seeded successfully"
