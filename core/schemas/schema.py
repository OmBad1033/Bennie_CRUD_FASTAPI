from pydantic import BaseModel, Extra, Field
from typing  import List,Optional

class productEntity(BaseModel):
    class Config:
        extra = Extra.forbid
        allow_population_by_field_name = True
    id: str 
    product_name:str
    product_price:int
    usecase:list

class ProductPayload(BaseModel):
    product_name:str
    product_price:int
    usecase:list

class ProductUpdatePayload(BaseModel):
    product_name:Optional[str]= Field(default=None)
    product_price:Optional[int]= Field(default=None)
    usecase:Optional[list]= Field(default=None)