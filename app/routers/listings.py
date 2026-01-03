from fastapi import APIRouter,Depends,Path
from sqlmodel import Session 
from typing import Annotated, Literal

from ..models import SuccessResponse, ListingBase,SwapBase
from ..db import get_session 
from ..repository import ListingRepository,SwapService,SwapRepository,BookRepository
from ..auth.security import get_current_user
from app.exceptions.custom import *

router = APIRouter(prefix="/listings",
                   tags =["Listing"])

listing_repo = ListingRepository()
book_repo = BookRepository()
service = SwapService(SwapRepository())

# Listing command
@router.post("",response_model = SuccessResponse)
def create_listing(book_id:int, 
                         current_user_id: int = Depends(get_current_user),
                         db:Session =Depends(get_session)):
    book = book_repo.get_book_sql(book_id,db)
    if book.owner_id != current_user_id:
        raise Unauthorized("Not authorized")
    listing_repo.create_listing_sql(book_id,db)
    return SuccessResponse(message="Successfully") 


@router.get("",response_model = list[ListingBase])
def get_listings(status: Literal["available","claimed","closed"],
                         db:Session = Depends(get_session)):
    return listing_repo.get_listings_sql(status,db)


@router.get("/{id}",response_model = ListingBase)
def get_a_listing(id:Annotated[int,Path()],db:Session =Depends(get_session)):
    return listing_repo.get_a_listing_sql(id,db)
     

@router.put("/{id}/close",response_model = SuccessResponse)
def close_listing(id:Annotated[int,Path()],
                        current_user_id: int = Depends(get_current_user),
                        db:Session = Depends(get_session)):
    book = book_repo.get_book_sql(id,db)
    if book.owner_id != current_user_id:
        raise Unauthorized("Not authorized")
    result = listing_repo.close_listings_sql(id,db)
    return SuccessResponse(message=result) 



# swap request 
@router.post("/{id}/swap",response_model = SuccessResponse)
def send_request(id: Annotated[int,Path()], message: str, db:Session = Depends(get_session), requester_id: int=Depends(get_current_user)):
    service.send_request(id,requester_id,message,db)
    return SuccessResponse(message="Posted successfully!") 

@router.get("/{id}/swaps",response_model = list[SwapBase])
def get_swap_list(id:Annotated[int,Path()],
                        db:Session = Depends(get_session)):
    return service.get_swap_list(id,db)
    

@router.post("/swaps/{swap_id}/respond",response_model=SuccessResponse)
def respond_request(swap_id: Annotated[int,Path()],
                          action: Literal["accept","reject"],
                          current_user_id: int = Depends(get_current_user),
                          db: Session = Depends(get_session)):
    result = service.respond_request(current_user_id,swap_id,action,db)
    return SuccessResponse(message=result) 