from fastapi import FastAPI,HTTPException

from .routers import users,books,listings,study_group,notifications
from .auth import login
from .models import SuccessResponse
from .exceptions.handlers import app_exception_handler,http_exception_handler
from .exceptions.custom import AppException
app = FastAPI()

# Import Routers 
app.include_router(users.router) 
app.include_router(books.router)
app.include_router(listings.router)
app.include_router(study_group.router) 
app.include_router(notifications.router) 
app.include_router(login.router)

#Import handler
app.add_exception_handler(AppException,app_exception_handler)
app.add_exception_handler(HTTPException,http_exception_handler)


@app.get("/health",response_model = SuccessResponse,description = "General State",response_model_exclude_none=True)
def check_health():
    return SuccessResponse(message="Perfect state")