from fastapi import APIRouter,Depends,Path
from sqlmodel import Session 
from typing import Annotated 

from ..models import UserCreate,UserRead,SuccessResponse
from ..db import get_session 
from ..repository import UserRepository 

user_repo = UserRepository()

router = APIRouter(prefix="/users",
                   tags=["User"])

@router.post("",response_model= SuccessResponse)
def create_user(user:UserCreate,db:Session = Depends(get_session)):
    user_repo.create_user_sql(user,db)
    return SuccessResponse(message="Created successfully!")

@router.get("/{user_id}",response_model=UserRead)
def get_user(user_id: Annotated[int,Path()],
                     db:Session = Depends(get_session)):
    return user_repo.get_user_sql(user_id,db)