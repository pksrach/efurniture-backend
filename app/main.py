import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config.custom_exceptions import ExceptionHandlerRegistry
from app.config.swagger import custom_openapi
from app.routes import auth
from app.routes.backend.base_backend import backend_router
from app.routes.frontend.base_frontend import frontend_router
from app.routes.seeding.seed_data import seed_router


def create_application():
    application = FastAPI()

    # Register exception handlers
    ExceptionHandlerRegistry.register_exception_handlers(application)

    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    # Serve the 'uploads' directory as static files
    application.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

    application.include_router(seed_router)
    application.include_router(frontend_router)
    application.include_router(auth.guest_router)
    application.include_router(backend_router)
    application.openapi = lambda: custom_openapi(application)
    return application


class MainApp:
    def __init__(self):
        self.app = create_application()
        self.configure_cors()
        self.add_routes()

    def configure_cors(self):
        origins = [
            "http://localhost:3000",
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,  # Allows requests from these origins
            allow_credentials=True,  # Allows cookies to be sent in cross-origin requests
            allow_methods=["*"],  # Allows all HTTP methods
            allow_headers=["*"],  # Allows all headers to be sent in requests
        )

    def add_routes(self):
        @self.app.get("/", include_in_schema=False)
        async def root():
            return {"message": "ok"}


main_app = MainApp()
app = main_app.app
