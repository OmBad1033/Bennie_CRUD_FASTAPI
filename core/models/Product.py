from pydantic import BaseModel,Field
from typing import Optional
from beanie import Document

class Product(Document):
    id: str = Field(alias="_id")
    product_name:str
    product_price:int
    usecase:list

    
    