import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from data.models import URL, USERS


class SQLiteSession:
    def __init__(self, path: str = "./data/TinyURL.sqlite") -> None:

        if os.path.exists(path):
            self.__engine = create_engine("sqlite:///" + path)
        else:
            raise FileNotFoundError

        session = sessionmaker(bind=self.__engine)
        self.__session = session()

    @property
    def connection_string(self) -> Session:
        return self.__session


if __name__ == "__main__":

    db_session = SQLiteSession().connection_string
    records = db_session.query(USERS).filter(
        USERS.ApiDevKey == "1d5997a5-0d7d-41e3-8de6-73ea144183e6"
    )
    for row in records:
        print(row)

    records = db_session.query(URL).all()
    for row in records:
        print(row)
