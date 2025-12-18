from sqlmodel import create_engine, Session

database_url = "postgresql+psycopg://postgres:ghasdfgh.09.za@localhost:8117/Bookswap"

engine = create_engine(
    database_url,
    echo = True
)

def get_session():
    with Session(engine) as session:
        yield session 
    