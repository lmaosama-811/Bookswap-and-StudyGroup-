from sqlmodel import create_engine, Session
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url:str
    secret_key:str  
    class Config:
        env_file =".env"
settings = Settings()

engine = create_engine(
    settings.database_url,
    echo = True
)


def get_session():
    with Session(engine) as session:
        yield session 
    