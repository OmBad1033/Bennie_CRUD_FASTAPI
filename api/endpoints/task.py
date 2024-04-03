from fastapi import APIRouter,Response,Depends,HTTPException
from starlette.requests import Request
from starlette import status
from fastapi.responses import HTMLResponse,RedirectResponse
from core.models.Product import Product
from uuid import uuid4
from core.schemas.schema import *
from core.config import Settings
from typing import List,Annotated

from core.services.auth import get_current_user

product=APIRouter()
setting=Settings()

user_dependency = Annotated[dict, Depends(get_current_user)]

@product.get("/read_by_name/{name}", response_model=productEntity)
async def readbyid(user: user_dependency, request: Request, name: str):
    if user:
        product = await Product.find_one(Product.product_name == name)
        if product:
            return product
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication Failed"
    )

@product.get("/read_all", response_model=List[productEntity])
async def readall(request: Request,user: user_dependency):
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication Failed"
    )
    products =await Product.find().to_list()
    return products

@product.post("/create", response_model=productEntity, response_model_by_alias=False)
async def create(user: user_dependency,request: Request, payload:ProductPayload):
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication Failed"
    )
    product=await Product(**payload.dict(), id=str(uuid4())).save()
    return product

@product.delete('/delete/{name}')
async def delete(user: user_dependency,request: Request,name:str):
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication Failed"
    )
    product =await Product.find_one(Product.product_name==name)
    if not product: return False
    else:
        await Product.delete(product)
        return True
    

@product.patch('/update/{name}')
async def update(user: user_dependency,request: Request,name:str,payload:ProductUpdatePayload):
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication Failed"
    )
    product = await Product.find_one(Product.product_name==name)
    if not product: return False
    update_data = {key: value for key, value in payload.dict().items() if value is not None}
    await product.update({"$set": update_data})
    return True






    