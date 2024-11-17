from sqlalchemy.ext.asyncio import AsyncSession

from app.services.seeding.seed_brand import SeedBrand
from app.services.seeding.seed_category import SeedCategory
from app.services.seeding.seed_color import SeedColor
from app.services.seeding.seed_location import SeedLocation
from app.services.seeding.seed_payment_method import SeedPaymentMethod
from app.services.seeding.seed_product import SeedProduct
from app.services.seeding.seed_user import SeedUser


async def seed_all(session: AsyncSession):
    await SeedUser(session).run()
    await SeedColor(session).run()
    await SeedCategory(session).run()
    await SeedBrand(session).run()
    await SeedLocation(session).run()
    await SeedPaymentMethod(session).run()
    await SeedProduct(session).run()

    return "Seeding all completed successfully."
