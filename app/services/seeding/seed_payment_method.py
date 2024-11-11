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
                "attachment_qr": "data:image/png;base64,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"
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
