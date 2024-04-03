from pydantic import BaseModel,Field
from typing import Optional
from beanie import Document

class Token(Document):
    access_token:str
    token_type:str