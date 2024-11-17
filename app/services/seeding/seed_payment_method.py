from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment_method import PaymentMethod


class SeedPaymentMethod:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def payment_method_exists(self, name: str) -> bool:
        stmt = select(PaymentMethod).filter(PaymentMethod.name == name)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def seed_payment_method(self):
        payment_methods = [
            {
                "name": "ABA Bank",
                "description": "ABA Bank payment method",
                "type": "Bank",
                "is_active": True,
                "transaction_fee": 0.0,
                "currency": "USD",
                "provider": "ABA Bank",
                "attachment_qr": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKQRwj2E41OLI2C2yvFnP0Yq30pcvi3zR3CA&s"
            },
            {
                "name": "Acelida",
                "description": "Acelida payment method",
                "type": "Bank",
                "is_active": True,
                "transaction_fee": 0.0,
                "currency": "USD",
                "provider": "Acelida",
                "attachment_qr": "https://www.acledabank.com.kh/kh/assets/image/qr-sticker.jpg"
            },
            {
                "name": "Canadia",
                "description": "Canadia Bank payment method",
                "type": "Bank",
                "is_active": True,
                "transaction_fee": 0.0,
                "currency": "USD",
                "provider": "Canadia Bank",
                "attachment_qr": "https://pppenglish.sgp1.digitaloceanspaces.com/image/main/canadiabank-3.jpg"
            },
            {
                "name": "Wing",
                "description": "Wing payment method",
                "type": "Online",
                "is_active": True,
                "transaction_fee": 1.0,
                "currency": "USD",
                "provider": "Wing",
                "attachment_qr": "https://www.wingbank.com.kh/wp-content/uploads/2024/06/khqr-img2.png"
            },
            {
                "name": "Chipmong",
                "description": "Chipmong payment method",
                "type": "Bank",
                "is_active": True,
                "transaction_fee": 0.0,
                "currency": "USD",
                "provider": "Chipmong",
                "attachment_qr": "https://www.chipmongbank.com/images/mobile-banking/qr-mobile-app.png"
            }
        ]

        for payment_method in payment_methods:
            if not await self.payment_method_exists(payment_method["name"]):
                new_payment_method = PaymentMethod(
                    name=payment_method["name"],
                    description=payment_method["description"],
                    type=payment_method["type"],
                    is_active=payment_method["is_active"],
                    transaction_fee=payment_method["transaction_fee"],
                    currency=payment_method["currency"],
                    provider=payment_method["provider"],
                    attachment_qr=payment_method["attachment_qr"]
                )
                self.session.add(new_payment_method)
            else:
                return "Payment methods already seeded."

    async def run(self):
        async with self.session.begin():
            await self.seed_payment_method()
        await self.session.commit()

        return "Payment Methods seeded successfully"
