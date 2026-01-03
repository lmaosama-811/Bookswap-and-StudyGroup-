from fastapi import HTTPException,status
from .models import *

allowed_table ={"users":User,"books":Book,"listings":Listing,"swap_requests":Swap,"study_groups":Group}
allowed_section = {"title":Book.title,"atuhor":Book.author,"condition":Book.condition,"description":Book.description}
allowed_filter = {"topic":Group.topic,"title":Group.title}

def validate_condition(request:str, allowed =["new","good","fair"]):
    if request not in allowed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid condition. Expect: new,good,fair")
    
def validate_section_book(section:str,
                          request:str,
                          allowed = ["author","title","description","condition"]):
    if section not in allowed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid section")
    elif section == "condition":
        validate_condition(request)
    return section 
