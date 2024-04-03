from fastapi import APIRouter,Response
from starlette.requests import Request
from fastapi.responses import HTMLResponse,RedirectResponse
from core.models.Product import Product
from uuid import uuid4
from core.schemas.schema import *
from core.config import Settings
from typing import List

product=APIRouter()

setting=Settings()

@product.get("/read_by_name/{name}",response_model=productEntity)
async def readbyid(request: Request,name:str):
    product =await Product.find_one(Product.product_name==name)
    return product

@product.get("/read_all", response_model=List[productEntity])
async def readall(request: Request):
    products =await Product.find().to_list()
    return products

@product.post("/create", response_model=productEntity, response_model_by_alias=False)
async def create(request: Request, payload:ProductPayload):
    product=await Product(**payload.dict(), id=str(uuid4())).save()
    return product

@product.delete('/delete/{name}')
async def delete(request: Request,name:str):
    product =await Product.find_one(Product.product_name==name)
    if not product: return False
    else:
        await Product.delete(product)
        return True
    

@product.patch('/update/{name}')
async def update(request: Request,name:str,payload:ProductUpdatePayload):
    product = await Product.find_one(Product.product_name==name)
    if not product: return False
    update_data = {key: value for key, value in payload.dict().items() if value is not None}
    await product.update({"$set": update_data})
    return True






    