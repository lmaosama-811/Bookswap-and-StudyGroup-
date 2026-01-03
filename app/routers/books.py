from fastapi import APIRouter,Depends,Path,Query
from sqlmodel import Session 
from typing import Annotated,Literal

from ..models import BookCreate,SuccessResponse,BookRead
from ..db import get_session 
from ..repository import BookRepository
from ..deps import validate_section_book
from app.auth.security import get_current_user
from ..exceptions.custom import *

router = APIRouter(prefix="/books",
                   tags = ["Books"])

book_repo=BookRepository()

@router.post("",response_model=SuccessResponse)
def create_book(book: BookCreate,db:Session = Depends(get_session)):
    book_repo.create_book_sql(book,db)
    return SuccessResponse(message="Book created successfully")

@router.get("/{book_id}",response_model=BookRead)
def get_book(book_id: Annotated[int,Path()],db:Session=Depends(get_session)):
   return book_repo.get_book_sql(book_id,db)

@router.get("",response_model = list[BookRead])
def get_list_book(owner_id:Annotated[int|None,Query()] = None,
                          limit: int = 10,
                          offset: int = 0,
                          db: Session = Depends(get_session)):
    return book_repo.get_list_book_sql(owner_id,limit,offset,db)
    
@router.put("/{book_id}",response_model =SuccessResponse)
def update_book(book_id:Annotated[int,Path()],
                      section:Literal["title","author","condition","description"],
                      request:str,
                      current_user_id: int =Depends(get_current_user),
                      db:Session = Depends(get_session)):
    book = book_repo.get_book_sql(book_id,db)
    if book.owner_id != current_user_id:
        raise Unauthorized("Not authorized")
    section_validated = validate_section_book(section,request)
    book_repo.update_book_sql(book_id,section_validated,request,db)
    return SuccessResponse(message="Successfully")

@router.delete("/{book_id}",response_model = SuccessResponse)
def delete_book(book_id:Annotated[int,Path()],
                      db:Session =Depends(get_session),
                      current_user_id:int = Depends(get_current_user)):
    book = book_repo.get_book_sql(book_id,db)
    if book.owner_id != current_user_id:
        raise Unauthorized("Not authorized")
    book_repo.delete_book_sql(book_id,db)
    return SuccessResponse(message="Successfully")