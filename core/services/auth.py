from datetime import timedelta,datetime
from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from starlette import status
from passlib.context import CryptContext 
from typing import Annotated
from jose import jwt,JWTError
from core.models.User import User
from core.models.Token import Token


router=APIRouter(
    prefix="/auth",
    tags=["auth"], 
)

SECRET_KEY ="12312j1198df38rf28rf239r23f2039r3f13"
ALGORITHM ="HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.post('/create_user', status_code=status.HTTP_201_CREATED)
async def create_current_user(create_user:User):
    hashed_password = bcrypt_context.hash(create_user.password)
    user = User(username=create_user.username, password=hashed_password)
    user_data = await user.save()
    return "USER ADDED"

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()]): 
    user=await authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token=create_access_token(user.username,timedelta(minutes=2))
    return {"access_token": token, "token_type":"bearer"}

async def authenticate(username:str, password:str):
    user=await User.find_one(User.username==username)
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(user:str,expires_delta:timedelta):
    encode={'sub':user}
    expires=datetime.utcnow() + expires_delta
    encode.update({'exp':expires})    
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)  


async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        if username is None:
            raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="user_invalid")
        return {'username':username} 
    except JWTError:
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="token_invalid")
