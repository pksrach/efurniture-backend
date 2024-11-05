from fastapi import APIRouter

frontend_product_router = APIRouter(
    prefix="/products",
    tags=["Frontend Product API"],
)


@frontend_product_router.get("", status_code=200)
async def get_products():
    return [
        {"name": "Product 1", "price": 100},
        {"name": "Product 2", "price": 200},
        {"name": "Product 3", "price": 300},
    ]
