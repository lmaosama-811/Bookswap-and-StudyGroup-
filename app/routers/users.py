from fastapi import APIRouter,Depends,Path
from sqlmodel import Session 
from typing import Annotated 

from ..models import User 
from ..db import get_session 
from ..respositories import create_user_sql,fetch_user_sql 

router = APIRouter(prefix="/users",
                   tags=["User"])

@router.post("",response_model= User)
async def create_user(user:User,db:Session = Depends(get_session)):
    new_user = create_user_sql(user,db)
    return new_user 

@router.get("/{user_id}",response_model=list[User])
async def fetch_user(user_id: Annotated[int,Path()],
                     db:Session = Depends(get_session)):
    list_users = fetch_user_sql(user_id, db)
    return list_users 
