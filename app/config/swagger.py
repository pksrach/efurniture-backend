from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="E-Furniture API",
        version="0.1.0",
        description="This is a very fancy project, with auto docs for the API and everything.",
        routes=app.routes,
    )
    openapi_schema["tags"] = [
        {"name": "Auth API", "description": "Operations for backend API"},

        {"name": "Backend Color API", "description": "Operations for color management in the backend"},
        {"name": "Backend Category API", "description": "Operations for category management in the backend"},
        {"name": "Backend Brand API", "description": "Operations for brand management in the backend"},
        {"name": "Backend Product API", "description": "Operations for product management in the backend"},
        {"name": "Backend User API", "description": "Operations for user management in the backend"},
        {"name": "Backend Customer API", "description": "Operations for customer management in the backend"},
        {"name": "Backend Payment Method API", "description": "Operations for payment method management in the backend"},
        {"name": "Backend Location API", "description": "Operations for location management in the backend"},
        {"name": "Backend Product Rate API", "description": "Operations for product rate management in the backend"},

        {"name": "Frontend API", "description": "Operations for frontend API"},
        {"name": "Default", "description": "Default operations"},
    ]

    openapi_schema["info"]["contact"] = {
        "name": "SETEC Institute",
        "url": "https://www.setecu.com",
    }
    openapi_schema["externalDocs"] = {
        "description": "Find more info here",
        "url": "https://fastapi.tiangolo.com",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
