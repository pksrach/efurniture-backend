import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config.swagger import custom_openapi
from app.routes import auth
from app.routes.backend.base_backend import backend_router
from app.routes.frontend.base_frontend import frontend_router
from app.routes.seeding import seed_user


def create_application():
    application = FastAPI()

    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    # Serve the 'uploads' directory as static files
    application.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    application.include_router(seed_user.seed_user_router)
    application.include_router(frontend_router)
    application.include_router(auth.guest_router)
    application.include_router(backend_router)
    application.openapi = lambda: custom_openapi(application)
    return application


origins = [
    "http://localhost:3000",
]

app = create_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from these origins
    allow_credentials=True,  # Allows cookies to be sent in cross-origin requests
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers to be sent in requests
)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "ok"}
