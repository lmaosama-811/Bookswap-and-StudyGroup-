from fastapi import APIRouter,Depends,Path,Query
from sqlmodel import Session 
from typing import Annotated, Literal, Union 

from ..models import Listing,Swap
from ..db import get_session 
from ..respositories import create_listing_sql, fetch_listings_sql,fetch_a_listing_sql,close_listings_sql,send_request_sql, fetch_swap_list_sql, respond_request_sql

router = APIRouter(prefix="/listings",
                   tags =["Listing"])

# listings
@router.post("")
async def create_listing(book_id:int, db:Session =Depends(get_session)):
    result =create_listing_sql(book_id,db)
    return result 

@router.get("",response_model = Union[list[Listing],dict])
async def fetch_listings(status: Literal["available","claimed","closed"],
                         db:Session = Depends(get_session)):
    result = fetch_listings_sql(status,db)
    return result if len(result) != 0 else {"message":"Not exist"}

@router.get("/{id}",response_model = Listing)
async def fetch_a_listing(id:Annotated[int,Path()],db:Session =Depends(get_session)):
    result = fetch_a_listing_sql(id,db)
    return result 

@router.put("/{id}/close")
async def close_listing(id:Annotated[int,Path()],db:Session = Depends(get_session)):
    result = close_listings_sql(id,db)
    return result 

# swap request 
@router.post("/{id}/swap")
async def send_request(id: Annotated[int,Path()], requester_id: int, message: str, db:Session = Depends(get_session)):
    result =send_request_sql(id,requester_id,message,db)
    return result 

@router.get("/{id}/swaps",response_model = list[Swap])
async def fetch_swap_list(id:Annotated[int,Path()],
                        db:Session = Depends(get_session)):
    result = fetch_swap_list_sql(id,db)
    return result 

@router.post("/swaps/{swap_id}/respond")
async def respond_request(swap_id: Annotated[int,Path()],
                          action: Literal["accept","reject"],
                          db: Session = Depends(get_session)):
    result = respond_request_sql(swap_id,action,db)
    return result 

