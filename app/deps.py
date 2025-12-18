from fastapi import HTTPException,status

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
