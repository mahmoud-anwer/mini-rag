from fastapi import APIRouter, Depends
from helpers import get_settings, Settings

# Creating an APIRouter instance with a prefix and tags
base_router = APIRouter(prefix="/api/v1", tags=["api_v1"])


@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    """
    Root endpoint for the base router.

    This endpoint returns the application name and version by extracting
    these details from the provided settings.

    Args:
        app_settings (Settings): Application settings dependency injection.

    Returns:
        dict: A dictionary containing the application name and version.
    """

    APP_NAME = app_settings.APP_NAME
    APP_VERSION = app_settings.APP_VERSION

    return {"application": APP_NAME, "version": APP_VERSION}
