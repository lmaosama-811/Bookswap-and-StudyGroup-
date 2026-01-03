from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError 
from passlib.context import CryptContext 

from ..db import settings 

security = OAuth2PasswordBearer(tokenUrl = "login")
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_current_user(token:str=Depends(security)):
    try:
        payload =jwt.decode(token,settings.secret_key,algorithms=["HS256"]) #return dict 
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code =401,detail ="Invalid token")
        return int(user_id) 
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")

def create_access_token(user_id:int):
    payload = {"sub":str(user_id)}
    return jwt.encode(payload,settings.secret_key,algorithm="HS256")

#Encode only receive 1 algorithm, decode can receive more => can be list

def hash_password(password:str) ->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)
