from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from api.api import api_router
from core.config import Settings
from core.models.model import __beanie_models__

from api.endpoints import task


app = FastAPI()
app.include_router(task.product)

settings = Settings()


@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    print(type(client))  

    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=__beanie_models__,
    )
    print("Success")
    






