from fastapi import APIRouter,Depends
from sqlmodel import Session 

from ..db import get_session
from ..models import Notifications
from ..respositories import read_notifications_sql 

router = APIRouter(prefix="/notifications",
                   tags =["Notifications"])

@router.get("",response_model = list[Notifications])
async def read_notifications(user_id:int,db:Session = Depends(get_session)):
    result = read_notifications_sql(user_id,db)
    return result 
