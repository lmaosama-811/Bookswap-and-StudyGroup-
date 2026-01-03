from pydantic import BaseModel,EmailStr
from datetime import datetime
from sqlmodel import SQLModel,Field, Column, DateTime,func

class User(SQLModel,table=True):
    __tablename__="users"
    id: int|None = Field(default = None, primary_key = True)
    username: str
    full_name: str| None = None 
    email: EmailStr| None = None 
    
class UserCreate(SQLModel):
    username: str
    full_name: str| None = None 
    email: EmailStr| None = None
    password: str 

class UserRead(SQLModel):
    id: int|None = None
    username: str
    full_name: str| None = None 
    email: EmailStr| None = None 

class Book(SQLModel,table =True):
    __tablename__="books"
    id: int|None = Field(default = None, primary_key =True)
    owner_id: int 
    title: str 
    author: str|None = None 
    condition: str
    description: str|None = None 
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True),server_default=func.now(),nullable=False))

class BookCreate(SQLModel):
    owner_id: int 
    title: str 
    author: str|None = None 
    condition: str
    description: str|None = None 


class BookRead(SQLModel):
    id: int|None = None
    owner_id: int 
    title: str 
    author: str|None = None 
    condition: str
    description: str|None = None 
    created_at: datetime 

class Listing(SQLModel,table = True):
    __tablename__ = "listings"
    id: int = Field(primary_key=True)
    book_id: int 
    status: str = "available"
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True),server_default=func.now(),nullable=False))

class ListingBase(SQLModel):
    book_id: int
    status: str
    created_at: datetime 

class Swap(SQLModel,table = True):
    __tablename__="swap_requests"
    id: int =Field(primary_key=True)
    listing_id: int
    requester_id: int 
    message: str| None = None 
    status: str = "pending"
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True),server_default=func.now(),nullable=False))

class SwapBase(SQLModel):
    listing_id: int 
    requester_id: int 
    message: str| None = None 
    status: str
    created_at: datetime 
    
class Group(SQLModel,table = True):
    __tablename__="study_groups"
    id: int =Field(primary_key=True)
    owner_id: int
    title: str
    topic: str|None = None 
    event_time: datetime| None = None
    capacity: int = 10 
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)) 

class GroupBase(SQLModel):
    owner_id: int 
    title: str
    topic: str|None = None 
    event_time: datetime
    capacity: int = 10 
    created_at: datetime 

class GroupMembers(SQLModel,table = True):
    __tablename__ = "study_group_members"
    id: int =Field(primary_key=True)
    group_id: int
    user_id: int
    joined_at: datetime = Field(sa_column=Column(DateTime(timezone=True),server_default=func.now(),nullable=False))

class Notifications(SQLModel,table = True):
    __tablename__="notifications"
    id: int = Field(primary_key=True)
    user_id: int 
    message: str

class NotificationsBase(SQLModel):
    message:str 

class SuccessResponse(BaseModel):
    success: bool = True 
    message: str
    data:dict|None = None 

class ErrorResponse(BaseModel):
    success: bool = False 
    error: str 
    code: int 

class Token(BaseModel):
    access_token:str
    token_type: str

class Accounts(SQLModel,table = True):
    __tablename__="accounts"
    user_id: int = Field(primary_key=True)
    username: str 
    password: str 