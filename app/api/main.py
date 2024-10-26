from fastapi import APIRouter

from app.api.routes import (
    brochures,
    items,
    login,
    users,
    utils,
    websites,
    brochures,
    temp,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(websites.router, prefix="/websites", tags=["websites"])
api_router.include_router(brochures.router, prefix="/brochures", tags=["brochures"])
api_router.include_router(temp.router, prefix="/temp", tags=["temp"])
