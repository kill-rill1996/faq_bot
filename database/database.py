from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import SQL_URL


engine = create_engine(f'{SQL_URL}', connect_args={"check_same_thread": False})

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
    print('Database created.')
