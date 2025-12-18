from sqlmodel import Session, text 
from fastapi import Depends,HTTPException,status,BackgroundTasks 
from typing import Literal,Annotated

from app.db import get_session 
from app.models import User,Book,Group

#Helper function related to database 
def check_id_exists(table_name:str,id_value:int,db:Session):
    allowed_table =["users","books","listings","swap_requests","study_groups"]

    if table_name not in allowed_table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid table name")
    
    sql =f"""
    SELECT 1 FROM {table_name}
    WHERE id =:id_value """
    cmd = text(sql).bindparams(id_value =id_value)
    result = db.exec(cmd)
    return result.first() is not None 

def send_notification(user_id:int,
                       message:str,
                       db:Session):
    sql ="""
    INSERT INTO notifications (user_id,message)
    VALUES (:user_id,:message)"""

    db.exec(text(sql).bindparams(user_id = user_id,message = message))
    db.commit()
    return 


#User command
def create_user_sql(user: User,db:Session):
    sql = """
    INSERT INTO users(username,full_name,email)
    VALUES (:username,:full_name,:email)
    RETURNING id,username,full_name,email"""

    cmd = text(sql).bindparams(username = user.username,
                               full_name = user.full_name,
                               email = user.email)
    result = db.exec(cmd)
    db.commit()

    return result.mappings().first()


def fetch_user_sql(user_id: int, db:Session):
    if not check_id_exists("users",user_id,db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    sql ="""
    SELECT id,username,full_name,email
    FROM users
    WHERE id = :user_id"""

    cmd = text(sql).bindparams(user_id = user_id)
    result = db.exec(cmd)
    return result.mappings().all()




#Book command
def create_book_sql(book:Book,db:Session):
    sql ="""
    INSERT INTO books(owner_id,title,author,condition,description)
    VALUES (:owner_id,:title,:author,:condition,:description)"""

    cmd = text(sql).bindparams(owner_id = book.owner_id,
                               title = book.title,
                               author = book.author,
                               condition = book.condition,
                               description = book.description)
    result = db.exec(cmd)
    db.commit()
    return {"message":"Successfully"}

def fetch_book_sql(book_id:int,db:Session):
    if not check_id_exists("books",book_id,db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
    sql ="""
    SELECT * FROM books
    WHERE id = :book_id"""
    
    cmd = text(sql).bindparams(book_id=book_id)
    result = db.exec(cmd)
    return result.mappings().all()

def fetch_list_book_sql(owner_id:int|None,limit:int,offset:int,db:Session):
    if owner_id is None:
        sql ="""
        SELECT * FROM books
        LIMIT :limit OFFSET :offset"""

        cmd = text(sql).bindparams(limit = limit,offset = offset)
    else:
        sql ="""
        SELECT * FROM books
        WHERE owner_id = :owner_id
        LIMIT :limit OFFSET :offset"""

        cmd = text(sql).bindparams(owner_id = owner_id,limit = limit,offset = offset)
    
    result = db.exec(cmd)
    return result.mappings().all()

def update_book_sql(book_id:int,section: str, request: str ,db:Session):
    if not check_id_exists("books",book_id,db):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Not found")
    sql =f"""
    UPDATE books
    SET {section} =:request
    WHERE id =:book_id"""
    cmd = text(sql).bindparams(request=request,
                               book_id=book_id)
    
    result = db.exec(cmd)
    db.commit()
    return {"message":"Successfully"}

def delete_book_sql(book_id:int,db:Session):
    if not check_id_exists("books",book_id,db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not Found")
    
    sql="""
    DELETE FROM books
    WHERE id =:book_id"""
    cmd = text(sql).bindparams(book_id=book_id)
    result = db.exec(cmd)
    db.commit()
    return {"message":"Successfully"}



#Listings command 
def create_listing_sql(book_id: int, db:Session):
    if not check_id_exists("books",book_id,db):
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND,detail="Book not found")
    sql="""
    INSERT INTO listings(book_id)
    VALUES (:book_id)"""

    cmd = text(sql).bindparams(book_id = book_id)
    result = db.exec(cmd)
    db.commit()
    return {"message":"Success"}

def fetch_listings_sql(status:Literal["available","claimed","closed"],
                   db:Session):
    sql ="""
    SELECT * FROM listings
    WHERE status = :status"""

    cmd = text(sql).bindparams(status =status)
    result = db.exec(cmd)

    return result.mappings().all()

def fetch_a_listing_sql(id:int,db:Session):
    if not check_id_exists("listings",id,db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    sql = """
    SELECT * FROM listings
    WHERE id = :id"""

    cmd = text(sql).bindparams(id = id)
    result = db.exec(cmd)
    return result.mappings().first()

def close_listings_sql(id:int,db:Session):
    if not check_id_exists("listings",id,db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    SQL = """
    SELECT status FROM listings
    WHERE id =:id"""
    check_status = db.exec(text(SQL).bindparams(id = id))
    row = check_status.mappings().first()
    if row['status'] == 'closed':
        return f"It has already closed"
    sql ="""
    UPDATE listings
    SET status = 'closed'
    WHERE id =:id"""
    db.exec(text(sql).bindparams(id = id))
    db.commit()
    return f"Success!!"




#Swap request 
def send_request_sql(id: int,requester_id: int, message: str,db:Session):
    if not check_id_exists("listings",id,db):
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="Exchange post not found")
    SQL = """
    SELECT status FROM listings
    WHERE id =:id"""
    check_status = db.exec(text(SQL).bindparams(id = id))
    row = check_status.mappings().first()
    if row['status'] != 'closed':
        return f"This exchange post is not available now!"
    sql ="""
    INSERT INTO swap_requests(listing_id,requester_id,message)
    VALUES (:id,:requester_id,:message)"""
    db.exec(text(sql).bindparams(id=id,
                                 requester_id=requester_id,
                                 message=message))
    db.commit()
    return f"Successfully posted!!!"
 
def fetch_swap_list_sql(id: int,db:Session):
    if not check_id_exists("swap_requests",id,db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    sql ="""
    SELECT * FROM swap_requests
    WHERE listing_id =:id"""
    result = db.exec(text(sql).bindparams(id=id))
    return result 

def respond_request_sql(swap_id: int,action:str, db:Session,):
    if action == "reject":
        sql ="""
        SELECT listing_id, requester_id FROM swap_requests
        WHERE id =:swap_id """

        result = db.exec(text(sql).bindparams(swap_id = swap_id))
        db.commit()
        record =result.mappings().first()
        message = f'Your swap request for listing ID {record["listing_id"]} has been rejected'
        send_notification(record["requester_id"],message,db)
        return f"You have rejected this request!!"
    else: 
        sql ="""
        UPDATE listings
        SET status = 'claimed'
        WHERE id =:swap_id"""
        db.exec(text(sql).bindparams(swap_id=swap_id))
        db.commit()

        sql ="""
        SELECT listing_id, requester_id FROM swap_requests
        WHERE id =:swap_id"""
        result =db.exec(text(sql).bindparams(swap_id = swap_id))
        record = result.mappings().first()
        message = f'Your swap request for listing ID {record["listing_id"]} has been accepted'
        send_notification(record["requester_id"],message,db)
        return f"You have accepted this request!!!"


#Group 
def create_group_sql(group:Group, db:Session):
    sql = """
    INSERT INTO study_groups(owner_id,title,topic,event_time,capacity)
    VALUES (:owner_id,:title,:topic,:event_time,:capacity)"""
    db.exec(text(sql).bindparams(owner_id=group.owner_id,
                                 title = group.title,
                                 topic =group.topic,
                                 event_time =group.event_time,
                                 capacity =group.capacity))
    db.commit()
    return f"Create successfully!!"

def fetch_group_sql(filter:str, request: str,db:Session):
    sql=f"""
    SELECT * FROM study_groups
    WHERE {filter} like :request"""
    result = db.exec(text(sql).bindparams(request= f"%{request}%"))
    return result.mappings().all()
    
def join_group_sql(group_id:int,user_id:int,db:Session):
    if not check_id_exists("study_groups",group_id,db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail ="Not Found")
    
    sql= """
    SELECT COUNT(*) FROM study_group_members
    WHERE group_id =:id"""
    number_of_members =db.exec(text(sql).bindparams(id = group_id)).scalar()

    sql ="""
    SELECT capacity FROM study_groups
    WHERE id =:id"""
    capacity = db.exec(text(sql).bindparams(id =group_id)).scalar()

    if number_of_members + 1 > capacity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Full.Please choose other group")
    
    sql ="""
    INSERT INTO study_group_members(group_id,user_id)
    VALUES (:group_id,:user_id)"""
    db.exec(text(sql).bindparams(group_id =group_id,user_id =user_id))
    db.commit()

    return f"You have joined this group successfully"

def leave_group_sql(group_id:int,user_id:int,db:Session):
    if not check_id_exists("study_groups",group_id,db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail ="Not Found")

    sql ="""
    DELETE FROM study_group_members
    WHERE user_id =:user_id AND group_id =:group_id"""

    db.exec(text(sql).bindparams(user_id =user_id,group_id=group_id))
    db.commit()
    return f"You have left group successfully!"



#Notifications
def read_notifications_sql(user_id:int, db:Session):
    sql ="""
    SELECT * FROM notifications
    WHERE user_id =:user_id"""
    result = db.exec(text(sql).bindparams(user_id=user_id))
    return result 
