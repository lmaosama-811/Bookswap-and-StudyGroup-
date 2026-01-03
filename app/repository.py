from sqlmodel import Session, text,select,update,delete,func,and_

from app.models import *
from app.deps import allowed_section,allowed_table,allowed_filter
from app.auth.security import hash_password,verify_password
from app.exceptions.custom import *


#Helper function related to database 
def check_id_exists(table_name:str,id_value:int,db:Session):
    check = allowed_table.get(table_name)
    if not check:
        raise NotFoundError("Invalid table name")
    
    cmd = select(1).where(check.id == id_value)
    return db.exec(cmd).first() is not None 

def send_notification(user_id:int,message:str,db:Session):
    new_notification = Notifications(user_id = user_id,message = message)
    db.add(new_notification)
    db.commit()
    return 

def authenticate_user(db:Session,username:str,password:str):
    stmt = select(Accounts).where(Accounts.username == username)
    account = db.exec(stmt).first()
    if account.username != username or not verify_password(password,account.password):
        raise Unauthorized("Invalid username or passwords")
    return account.user_id

def check_user_available_in_group(db: Session,user_id: int,group_id: int) -> bool:
    cmd = select(1).where(GroupMembers.user_id == user_id,GroupMembers.group_id == group_id)
    return db.exec(cmd).first() is None

    
class UserRepository:
    def create_user_sql(self,user:UserCreate,db:Session):
        stmt = select(1).where(User.username==user.username)
        check = db.exec(stmt)
        if check.first() is not None:
            raise BadRequestError("This user has already existed!")
        
        new_user = User(username=user.username,full_name=user.full_name,email=user.email)
        db.add(new_user)
        db.flush()
        
        hashed_password = hash_password(user.password)
        db.add(Accounts(user_id = new_user.id,username=user.username,password=hashed_password))
        db.commit()
        return


    def get_user_sql(self,user_id: int, db:Session):
        if not check_id_exists("users",user_id,db):
            raise NotFoundError("User not found")
        return db.get(User,user_id)


class BookRepository:
    def create_book_sql(self,book:BookCreate,db:Session) -> None:
        new_book = Book(owner_id=book.owner_id,title=book.title,author=book.author,condition=book.condition,description=book.description)
        db.add(new_book)
        db.commit()
        return 

    def get_book_sql(self,book_id:int,db:Session):
        if not check_id_exists("books",book_id,db):
            raise NotFoundError("Book not found")
        return db.get(Book,book_id)
        

    def get_list_book_sql(self,owner_id:int|None,limit:int,offset:int,db:Session):
        if owner_id is None:
            cmd = select(Book).order_by(Book.id).limit(limit).offset(offset)
        else:
            cmd = select(Book).where(Book.owner_id == owner_id).order_by(Book.id).limit(limit).offset(offset)
        result = db.exec(cmd)
        return result.all()
    

    def update_book_sql(self,book_id:int,section: str, request: str ,db:Session) -> None:
        if not check_id_exists("books",book_id,db):
            raise NotFoundError("Book not found")
        check = allowed_section.get(section)
        if not check:
            raise BadRequestError("Invalid section")

        cmd = update(Book).where(Book.id == book_id).values({check: request})
        db.exec(cmd)
        db.commit()
        return

    def delete_book_sql(self,book_id:int,db:Session) -> None:
        if not check_id_exists("books",book_id,db):
            raise NotFoundError("Book not Found")
        stmt = delete(Book).where(Book.id == book_id)
        db.exec(stmt)
        db.commit()
        return 



class ListingRepository: 
    def create_listing_sql(self,book_id: int,db:Session) -> None:
        if not check_id_exists("books",book_id,db):
            raise NotFoundError("Book not found")
        
        new_listing = Listing(book_id = book_id)
        db.add(new_listing)
        db.commit()
        return 

    def get_listings_sql(self,status:str,db:Session):
        cmd = select(Listing).where(Listing.status == status)
        return db.exec(cmd).all() 

    def get_a_listing_sql(self,id:int,db:Session):
        if not check_id_exists("listings",id,db):
            raise NotFoundError("Listing not Found")

        cmd = select(Listing).where(Listing.id == id)
        return db.exec(cmd).first()

    def close_listings_sql(self,id:int,db:Session):
        if not check_id_exists("listings",id,db):
            raise NotFoundError("Listing not Found")
        
        check_status = db.get(Listing,id)
        if check_status.status == 'closed':
            return "This section has already be closed!"
        
        cmd = update(Listing).where(Listing.id == id).values(status='closed')
        db.exec(cmd)
        db.commit()
        return "Successfully"


class SwapRepository:
    def create_swap_request(self, listing_id: int, requester_id: int, message: str, db: Session) -> None:
        new_request = Swap(listing_id = listing_id,requester_id=requester_id,message=message)
        db.add(new_request)
        db.commit()
        return 
    
    def get_listing_status(self, listing_id: int, db: Session) -> str | None:
        cmd = select(Listing.status).where(Listing.id == listing_id)
        return db.exec(cmd).one_or_none()

    def get_swap(self, swap_id: int, db: Session):
        cmd = select(Swap.listing_id,Swap.requester_id).where(Swap.id == swap_id)
        return db.exec(cmd).first()
        

    def get_swaps_by_listing(self, listing_id: int, db: Session):
        cmd = select(Swap).where(Swap.listing_id==listing_id)
        return db.exec(cmd).all()

    def get_listing_owner(self, swap_id: int, db: Session) -> int | None:
        cmd = (select(Book.owner_id)
               .join(Listing, Book.id == Listing.book_id)
               .join(Swap, Listing.id == Swap.listing_id)
               .where(Swap.id == swap_id))
        return db.exec(cmd).one_or_none()

    def update_listing_status(self, listing_id: int, status: str, db: Session) -> None:
        cmd = update(Listing).where(Listing.id == listing_id).values(status = status)
        db.exec(cmd)
        db.commit()
        return 
    

class SwapService:
    def __init__(self, swap_repo: SwapRepository):
        self.swap_repo = swap_repo

    def send_request(self, listing_id: int, requester_id: int, message: str, db: Session) -> None:
        if not check_id_exists("listings", listing_id, db):
            raise NotFoundError("Exchange post not found")

        status = self.swap_repo.get_listing_status(listing_id, db)
        if status != "available":
            raise BadRequestError("This exchange post is not available now")

        self.swap_repo.create_swap_request(listing_id, requester_id, message, db)
        db.commit()

    def get_swap_list(self, listing_id: int, db: Session):
        if not check_id_exists("listings", listing_id, db):
            raise NotFoundError("Exchange post not found")

        return self.swap_repo.get_swaps_by_listing(listing_id, db)

    def respond_request(self, user_id: int, swap_id: int, action: str, db: Session):
        if not check_id_exists("swap_requests", swap_id, db):
            raise NotFoundError("Swap request not found")

        owner_id = self.swap_repo.get_listing_owner(swap_id, db)
        if user_id != owner_id:
            raise Unauthorized("Not authorized")

        swap = self.swap_repo.get_swap(swap_id, db)

        if action == "reject":
            message = f"Your swap request for listing ID {swap.listing_id} has been rejected"
            send_notification(swap.requester_id, message, db)
            return "You have rejected this request"

        if action == "accept":
            self.swap_repo.update_listing_status(swap.listing_id, "claimed", db)
            db.commit()

            message = f"Your swap request for listing ID {swap.listing_id} has been accepted"
            send_notification(swap.requester_id, message, db)
            return "You have accepted this request"

        raise BadRequestError("Invalid action")




class GroupRepository: 
    def create_group_sql(self,group:GroupBase, db:Session) -> None:
        new_group = Group(owner_id=group.owner_id,
                          title=group.title,
                          topic=group.topic,
                          event_time=group.event_time,
                          capacity=group.capacity)
        db.add(new_group)
        db.commit()
        return 


    def get_group_sql(self,filter:str, request: str,db:Session):
        check = allowed_filter.get(filter)
        cmd = select(Group).where(check.like(f"%{request}%"))
        return db.exec(cmd).all()
        

    def join_group_sql(self,group_id:int,user_id:int,db:Session) -> None:
        if not check_id_exists("study_groups",group_id,db):
            raise NotFoundError("Group not Found")
        
        check = check_user_available_in_group(db,user_id,group_id)
        if not check:
            raise BadRequestError("You've already been in this group")
        

        cmd = select(func.count()).where(GroupMembers.group_id == group_id)
        number_of_members = db.exec(cmd).first()
        
        cmd = select(Group.capacity).where(Group.id == group_id)
        capacity = db.exec(cmd).first()

        if number_of_members + 1 > capacity:
            raise BadRequestError("Full !! Please choose other group")
        
        new_member = GroupMembers(group_id=group_id,
                                  user_id=user_id)
        db.add(new_member)
        db.commit()
        return 


    def leave_group_sql(self,group_id:int,user_id:int,db:Session) -> None:
        if not check_id_exists("study_groups",group_id,db):
            raise NotFoundError("Group not Found")
        
        check = check_user_available_in_group(db,user_id,group_id)
        if check:
            raise BadRequestError("You've not joined this group -> Can not leave")

        cmd = delete(GroupMembers).where(and_(GroupMembers.user_id == user_id,GroupMembers.group_id == group_id))
        db.exec(cmd)
        db.commit()
        return 



class Notification_Repository:
    def read_notifications_sql(self,user_id:int, db:Session):
        cmd = select(Notifications).where(Notifications.user_id==user_id)
        return db.exec(cmd).all()