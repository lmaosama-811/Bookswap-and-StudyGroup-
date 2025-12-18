from fastapi import APIRouter,Depends,Path,Query
from sqlmodel import Session 
from typing import Annotated,Literal

from ..models import Book 
from ..db import get_session 
from ..respositories import create_book_sql,fetch_book_sql,fetch_list_book_sql,update_book_sql,delete_book_sql
from ..deps import validate_section_book

router = APIRouter(prefix="/books",
                   tags = ["Books"])

@router.post("")
async def create_book(book: Book,db:Session = Depends(get_session)):
    new_book = create_book_sql(book,db)
    return new_book

@router.get("/{book_id}",response_model=list[Book])
async def fetch_book(book_id: Annotated[int,Path()],db:Session=Depends(get_session)):
    book = fetch_book_sql(book_id,db)
    return book

@router.get("",response_model = list[Book])
async def fetch_list_book(owner_id:Annotated[int|None,Query()] = None,
                          limit: int = 10,
                          offset: int = 0,
                          db: Session = Depends(get_session)):
    list_book = fetch_list_book_sql(owner_id,limit,offset,db)
    return list_book 

@router.put("/{book_id}")
async def update_book(book_id:Annotated[int,Path()],
                      section:Literal["title","author","condition","description"],
                      request:str,
                      db:Session = Depends(get_session)):
    section_validated = validate_section_book(section,request)
    result = update_book_sql(book_id,section_validated,request,db)
    return result 

@router.delete("/{book_id}")
async def delete_book(book_id:Annotated[int,Path()],
                      db:Session =Depends(get_session)):
    result = delete_book_sql(book_id,db)
    return result 
