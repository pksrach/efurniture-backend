from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category


class SeedCategory:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def category_exists(self, name: str) -> bool:
        stmt = select(Category).filter(Category.name == name)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def seed_category(self):
        categories = [
            {"name": "Sofa",
             "attachment": "https://www.bludot.com/media/catalog/product/g/u/gu1_82sfwo_oa_frontlow_default.jpg?optimize=medium&fit=bounds&height=1200&width=1500&canvas=1500:1200"},
            {"name": "Couch",
             "attachment": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcT1W98tvl_tblhMpUygGIqD-WJA7dfs0txp-uRTplU4EJDZCtW8wczao_chCt4I"},
            {"name": "Chair",
             "attachment": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3nQ3CERFkb0irPgy2m8hB5jNvJXvfG_VOKyxTIQFDbOG0_CZnsEgaiWO-5TC1"},
            {"name": "Armchair",
             "attachment": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRurwoI0Itnozqal3J_g-2CcIuzyD5dU-Ve7AzvI_z6xcp2hfgb3nmnhxt2N4rK"},
            {"name": "Recliner",
             "attachment": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSRkLxipz-xXNXLnhd7-QARv3bkdiArLh9teyByb2WzFpBNbZnS6R5tKEuro7X-"},
            {"name": "Ottoman",
             "attachment": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcRSb0P_OXiqt9rHt034hn6n-TfDKLm1LU3p852rPfsfZLI-GAHingUBrmK0jap0"},
            {"name": "Bench",
             "attachment": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTgeZkaT5xRukuPpNRYtIucXjGVml-px1XrSP83NflqZTYBaEqXXNRFF0L3pWpa"},
            {"name": "Stool",
             "attachment": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVH6E37x2Wi_p76hJkxasSAo6ZEf1MoXiXmsbIc36HwnuqQuRuA1dNZ4cRsh6y"},
            {"name": "Wardrobe",
             "attachment": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQqrMJj2tuhKpbNLeAKsQzsHUH8jhlQKpwJSgIzsS97sz8nQqSQgPf0bPx4WWW_"},
            {"name": "Dresser",
             "attachment": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQPJEeqvf45j-HMKH1_A61dlpobB5yig_BYjQ3VttLrZS_xUu3hBTyNi7pxqyDy"},
            {"name": "Chest of Drawers",
             "attachment": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSV3JvBz_a4xS0PotubS7c3SNETEUaeMX0QMlSOinKXHEXkT_ppEM11PqpEBM5i"},
            {"name": "Bookshelf",
             "attachment": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTCJ_5TYhgD7_4QCyGlz7_yNQ8GCQVOOLfQkbjhYp0N3cA6JDCxVpjhXvIf86Rg"},
            {"name": "Cabinet",
             "attachment": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSxzJVXNAZRUvQkG7-laW1py_xckyjiTiJpYt8GUSAHuRgAo2YWWUyxG6Z5OSfa"},
            {"name": "Dining Table",
             "attachment": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcRN3gfxPvpzXuOvl9CAVkpSV82TaSAqLm5lamS7EA7GMPd5FhpKMgoR8_YSzmXb"},
            {"name": "Coffee Table",
             "attachment": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSFWC44v9rxIWkOPEpzkIfTfv-SQ1LarQg3BGM0QUn73fsKuEAEN2emPRXhh5X_"},
            {"name": "End Table",
             "attachment": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcQzp_HgLrDBYTfo6IFizjmdQvYnV3aPd-SuhaxUzx9pMBc5JVfM7T4mgycDIk6W"},
            {"name": "Side Table",
             "attachment": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSMk_zWj30hYPfxoCUgZKkT4kGMFPHShyS7jQ5J4L0or96DsU7ZBnsGOps1jRqL"},
            {"name": "Console Table",
             "attachment": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRa4MFPVpBJFyp8ha7s68-13dhRPF7whsAAyfyHS_ij5sttcNXfgCBpOou68HDD"},
            {"name": "Bed",
             "attachment": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTy87XZuKpzeRrBUpVGsubCpi-hyTWECZyHrQ9S5_Bb_-YU9VmZIi1KqY-3thmM"},
            {"name": "Bed Frame",
             "attachment": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcToga6OZv_NKsENzQ1iay9CFbyZOTxbYMhe3rCcOj409qaIafT1oegiL-ZjtiD4"},
            {"name": "Mattress",
             "attachment": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcS2j1u1mSin448wzfxlgHesU2cvTdioeYmbrdfu0Q1dqO5yGlHtvfErnDLc9Uv4"},
            {"name": "Box Spring",
             "attachment": "https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcS1aKtio8eTUipds1ux0mgS4ZGi36NcOlCnf-bSyVzHpZxGdsCEnlpHRF4wBUhz"},
        ]

        for category in categories:
            if not await self.category_exists(category["name"]):
                new_category = Category(
                    name=category["name"],
                    attachment=category["attachment"]
                )
                self.session.add(new_category)
            else:
                return "Categories already seeded."

    async def run(self):
        async with self.session.begin():
            await self.seed_category()
        await self.session.commit()

        return "Categories seeded successfully"
