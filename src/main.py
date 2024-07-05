from fastapi import FastAPI
from routes import base_router, data_router

# Creating an instance of the FastAPI class
app = FastAPI()

# Including the base_router ("/api/v1")
app.include_router(base_router)

# Including the data_router ("/api/v1/data")
app.include_router(data_router)
