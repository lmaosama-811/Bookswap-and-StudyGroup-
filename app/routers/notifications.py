from fastapi import APIRouter,Depends
from sqlmodel import Session 

from ..db import get_session
from ..models import NotificationsBase
from ..repository import Notification_Repository
from ..auth.security import get_current_user

router = APIRouter(prefix="/notifications",
                   tags =["Notifications"])

note_repo =Notification_Repository()

@router.get("",response_model = list[NotificationsBase])
def read_notifications(current_user_id:int =Depends(get_current_user),
                             db:Session = Depends(get_session)):
    return note_repo.read_notifications_sql(current_user_id,db)