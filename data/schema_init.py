from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker

Base = declarative_base()


class URL(Base):
    __tablename__ = "url"
    EncodedURL = Column(String, primary_key=True)
    OriginalURL = Column(String)
    CreationDate = Column(DateTime)
    ExpirationDate = Column(DateTime)
    UserID = Column(Integer, ForeignKey("users.UserID"))

    def __repr__(self):
        return (
            "<User(UserID='%s', EncodedURL='%s', OriginalURL='%s', CreationDate='%s', ExpirationDate='%s')>"
            % (
                self.UserID,
                self.EncodedURL,
                self.OriginalURL,
                str(self.CreationDate),
                str(self.ExpirationDate),
            )
        )


class USERS(Base):
    __tablename__ = "users"
    UserID = Column(Integer, primary_key=True)
    Name = Column(String)
    Email = Column(String)
    CreationDate = Column(DateTime)
    LastLogin = Column(DateTime)

    def __repr__(self):
        return (
            "<User(UserID='%s', Name='%s', Email='%s', CreationDate='%s', LastLogin='%s')>"
            % (
                self.UserID,
                self.Name,
                self.Email,
                str(self.CreationDate),
                str(self.LastLogin),
            )
        )


if __name__ == "__main__":

    ## Creation of Tables
    engine = create_engine("sqlite:///./data/TinyURL.sqlite")
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    ## Insertions
    session = session()
    one_url = URL(
        EncodedURL="asdfae2",
        OriginalURL="https://www.hello.com",
        CreationDate=datetime.today(),
        ExpirationDate=datetime.today(),
        UserID=1412,
    )
    one_user = USERS(
        UserID=1412,
        Name="John Doe",
        Email="john.doe@xmen.com",
        CreationDate=datetime.today(),
        LastLogin=datetime.now(),
    )
    # print(one_user)
    session.add(one_user)
    session.add(one_url)
    session.commit()

    for row in session.query(URL).order_by(URL.EncodedURL):
        print(row)

    for row in session.query(USERS).order_by(USERS.UserID):
        print(row)
