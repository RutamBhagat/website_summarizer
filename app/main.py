import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import settings

# Add database initialization to startup
from app.core.db import init_db
from sqlmodel import Session
from app.core.db import engine
import os


def custom_generate_unique_id(route: APIRoute) -> str:
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],  # Add this
        max_age=3600,  # Add this
    )


# add a root and healthcheck route
@app.get("/")
async def root_route():
    return {"message": "Welcome to the FastAPI app!"}


@app.head("/")
async def root_head():
    return {"message": "This is a HEAD request"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(api_router, prefix=settings.API_V1_STR)


# Add database initialization to startup
@app.on_event("startup")
async def on_startup():
    print("CORS Origins:", settings.all_cors_origins)  # Debug print
    with Session(engine) as session:
        init_db(session)
