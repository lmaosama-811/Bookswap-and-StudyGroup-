from pydantic import BaseModel, Field,EmailStr
from typing import Annotated, Literal 
from datetime import datetime

class User(BaseModel):
    username: str
    full_name: str| None = None 
    email: EmailStr| None = None 

class Book(BaseModel):
    owner_id: int 
    title: str 
    author: str|None = None 
    condition: Literal["new","good","fair"]
    description: str|None = None 
    created_at: datetime 

class Listing(BaseModel):
    book_id: int 
    status: Literal["available","claimed","closed"]
    created_at: datetime 

class Swap(BaseModel):
    listing_id: int 
    requester_id: int 
    message: str| None = None 
    status: Literal["pending","accepted","rejected"]
    created_at: datetime 
    
class Group(BaseModel):
    owner_id: int 
    title: str
    topic: str|None = None 
    event_time: datetime
    capacity: int = 10 
    created_at: datetime 

class Notifications(BaseModel):
    message:str 