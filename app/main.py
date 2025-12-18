from fastapi import FastAPI
from .routers import users,books,listings,study_group,notifications
app = FastAPI()

app.include_router(users.router)
app.include_router(books.router)
app.include_router(listings.router)
app.include_router(study_group.router)
app.include_router(notifications.router)

@app.get("/health",description = "General State")
def check_health():
    return {"Connection":"ok",
            "Database":"ok"}
