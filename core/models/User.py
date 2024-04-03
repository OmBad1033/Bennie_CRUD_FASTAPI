from pydantic import BaseModel,Field
from typing import Optional
from beanie import Document

class User(Document):
    username:str
    password:str
   