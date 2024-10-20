from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="E-Furniture API",
        version="0.1.0",
        description="API documentation for E-Furniture platform, providing access to backend and frontend operations for managing products, users, and more.",
        routes=app.routes,
    )
    openapi_schema["tags"] = [
        {"name": "Auth API", "description": "Authentication and authorization operations."},

        {"name": "Backend Color API", "description": "Endpoints for managing color-related data in the backend."},
        {"name": "Backend Category API", "description": "Endpoints for managing categories in the backend."},
        {"name": "Backend Brand API", "description": "Endpoints for managing brands in the backend."},
        {"name": "Backend Product API", "description": "Endpoints for managing product details in the backend."},
        {"name": "Backend User API", "description": "Endpoints for managing user accounts and roles in the backend."},
        {"name": "Backend Customer API", "description": "Endpoints for managing customer information in the backend."},
        {"name": "Backend Payment Method API", "description": "Endpoints for managing payment method information in the backend."},
        {"name": "Backend Product Rate API", "description": "Endpoints for managing product rate information in the backend."},
        {"name": "Backend Location API", "description": "Endpoints for managing location information in the backend."},
        {"name": "Backend Media Storage API", "description": "Endpoints for managing media storage information in the backend."},

        {"name": "Frontend API", "description": "Endpoints used for frontend operations and interactions."},
        {"name": "Default", "description": "Default operations provided by the system."},
    ]

    openapi_schema["info"]["contact"] = {
        "name": "SETEC Institute",
        "url": "https://www.setecu.com",
    }
    openapi_schema["externalDocs"] = {
        "description": "Additional information can be found here.",
        "url": "https://fastapi.tiangolo.com",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
