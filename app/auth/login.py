from fastapi import APIRouter,Depends 
from fastapi.security import OAuth2PasswordRequestForm 
from typing import Annotated 
from sqlmodel import Session

from .security import create_access_token
from ..db import get_session
from ..repository import authenticate_user
from ..models import Token 

router =APIRouter()

@router.post("/login")
def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()], db:Session=Depends(get_session)):
    user_id =authenticate_user(db,form_data.username,form_data.password)
    access_token = create_access_token(user_id)
    return Token(access_token=access_token,token_type="bearer")
