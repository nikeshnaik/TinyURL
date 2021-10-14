import random
from typing import Optional

from fastapi import HTTPException
from hashids import Hashids

from data.database import SQLiteSession
from data.models import URL, USERS
from tinyurl.exception_handling import DataError
from tinyurl.logging import turl_logger


def get_user_apidevkey(user_name: str, email: str) -> bool:

    if not user_name or not email:
        raise ValueError("User name or email must not be none")

    db_session = SQLiteSession().connection_string
    user_record = (
        db_session.query(USERS)
        .filter(USERS.Name == user_name, USERS.Email == email)
        .one()
    )
    db_session.close()

    return user_record.ApiDevKey
