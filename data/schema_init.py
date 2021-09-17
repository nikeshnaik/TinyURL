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
    hash = Column(String, primary_key=True)
    OriginalURL = Column(String)
    CreationDate = Column(DateTime)
    ExpirationDate = Column(DateTime)
    UserID = Column(Integer)


class USERS(Base):
    __tablename__ = "users"
    UserID = Column(Integer, primary_key=True)
    Name = Column(String)
    Email = Column(String)
    CreationDate = Column(DateTime)
    LastLogin = Column(DateTime)

    url = relationship(
        URL, backref=backref("users", uselist=True, cascade="delete,all")
    )


engine = create_engine("sqlite:///./data/TinyURL.sqlite")
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


## use cassandra