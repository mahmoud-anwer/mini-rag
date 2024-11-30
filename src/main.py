from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers import get_settings
from routes import base_router, data_router


# Creating an instance of the FastAPI class
app = FastAPI()

# A FastAPI event to connect to DB on app startup
@app.on_event("startup")
async def startup_db_client():
    """
        This function gets the application connect to DB at startup event.
    """
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

# A FastAPI event to close the connection to DB on app shutdown
@app.on_event("shutdown")
async def shutdown_db_client():
    """
        This function closes the connection with DB at shutdown event .
    """
    app.mongo_conn.close()

# Including the base_router ("/api/v1")
app.include_router(base_router)

# Including the data_router ("/api/v1/data")
app.include_router(data_router)
