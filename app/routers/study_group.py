from fastapi import APIRouter,Depends,Path,Query
from sqlmodel import Session 
from typing import Annotated, Literal, Union 

from ..models import Group
from ..db import get_session 
from ..respositories import create_group_sql,fetch_group_sql,join_group_sql,leave_group_sql

router = APIRouter(prefix ="/groups",
                   tags=['Study groups'])

@router.post("")
async def create_group(group:Group, db:Session= Depends(get_session)):
    result = create_group_sql(group,db)
    return result 

@router.get("",response_model = list[Group])
async def fetch_group(filter:Literal["topic","title"],
                      request: str,
                      db:Session = Depends(get_session)):
    result = fetch_group_sql(filter,request,db)
    return result 

@router.post("/{group_id}/join")
async def join_group(group_id:Annotated[int,Path()],
                     user_id: int,
                     db:Session = Depends(get_session)):
    result = join_group_sql(group_id,user_id,db)
    return result 

@router.post("/{group_id}/leave")
async def leave_group(group_id:Annotated[int,Path()],
                     user_id: int,
                     db:Session = Depends(get_session)):
    result = leave_group_sql(group_id,user_id,db)
    return result 
