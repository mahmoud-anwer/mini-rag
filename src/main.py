from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers import get_settings
from routes import base_router, upload_router, process_router, nlp_router
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser


# Creating an instance of the FastAPI class
app = FastAPI()

# A FastAPI event to connect to DB on app startup
@app.on_event("startup")
async def startup_span():
    """
        This function gets the application connect to DB at startup event.
    """
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(settings)

    # generation client
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    # embedding client
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)

    # vector db client
    app.vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vectordb_client.connect()

    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,

    )

# A FastAPI event to close the connection to DB on app shutdown
@app.on_event("shutdown")
async def shutdown_span():
    """
        This function closes the connection with DB at shutdown event .
    """
    app.mongo_conn.close()
    app.vectordb_client.disconnect()

# A FastAPI event to connect to DB on app startup
# app.router.lifespan.on_startup.append(startup_db_client)

# A FastAPI event to close the connection to DB on app shutdown
# app.router.lifespan.on_shutdown.append(shutdown_db_client)


# Including the base_router ("/api/v1")
app.include_router(base_router)

# Including the upload_router ("/api/v1/data")
app.include_router(upload_router)

# Including the process_router ("/api/v1/data")
app.include_router(process_router)

# Including the nlp_router ("/api/v1/nlp")
app.include_router(nlp_router)
