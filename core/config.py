from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #MONGO_URI: str = 'mongodb+srv://ombad:messi1033om@cluster0.aqbw0sc.mongodb.net'
    MONGO_URI: str = 'mongodb://localhost:27017'
    DATABASE_NAME: str = 'FastAPI'
    COLLECTION_NAME:str = 'test'

