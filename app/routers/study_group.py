from fastapi import APIRouter,Depends,Path
from sqlmodel import Session 
from typing import Annotated, Literal

from ..models import GroupBase, SuccessResponse
from ..db import get_session 
from ..repository import GroupRepository
from ..auth.security import get_current_user

router = APIRouter(prefix ="/groups",
                   tags=['Study groups'])

group_repo=GroupRepository()

@router.post("",response_model =SuccessResponse)
def create_group(group:GroupBase, db:Session= Depends(get_session)):
    group_repo.create_group_sql(group,db)
    return SuccessResponse(message="Created successfully")


@router.get("",response_model = list[GroupBase])
def get_group(filter:Literal["topic","title"],
                      request: str,
                      db:Session = Depends(get_session)):
    return group_repo.get_group_sql(filter,request,db)
    

@router.post("/{group_id}/join",response_model = SuccessResponse)
def join_group(group_id:Annotated[int,Path()],
                     user_id: int = Depends(get_current_user),
                     db:Session = Depends(get_session)):
    group_repo.join_group_sql(group_id,user_id,db)
    return SuccessResponse(message="You have joined this group successfully")


@router.post("/{group_id}/leave",response_model =SuccessResponse)
def leave_group(group_id:Annotated[int,Path()],
                     user_id: int = Depends(get_current_user),
                     db:Session = Depends(get_session)):
    group_repo.leave_group_sql(group_id,user_id,db)
    return SuccessResponse(message="You have left group successfully!")