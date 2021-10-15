import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from data.models import URL, USERS

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/TinyURL.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":

    db_session = SessionLocal()
    records = db_session.query(USERS).all()
    for row in records:
        print(row)

    records = db_session.query(URL).all()
    for row in records:
        print(row)
