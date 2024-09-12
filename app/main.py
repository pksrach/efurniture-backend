from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user
from app.routes.seeding import seed_user
from app.config.swagger import custom_openapi


def create_application():
    application = FastAPI()
    application.include_router(seed_user.seed_user_router)
    application.include_router(user.user_router)
    application.include_router(user.guest_router)
    application.include_router(user.auth_router)
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