from fastapi import APIRouter

product_router = APIRouter(
    prefix="/products"
)


@product_router.get("", status_code=200, response_model=list)
async def get_products():
    return [
        {"name": "Product 1", "price": 100},
        {"name": "Product 2", "price": 200},
        {"name": "Product 3", "price": 300},
    ]
