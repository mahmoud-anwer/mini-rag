from fastapi import APIRouter, Depends
from helpers.config import get_settings, Settings

base_router = APIRouter(prefix="/api/v1", tags=["api_v1"])

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    APP_NAME=app_settings.APP_NAME
    APP_VERSION=app_settings.APP_VERSION
    return {
        "application": APP_NAME,
        "version": APP_VERSION
    }
