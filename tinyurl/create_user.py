import random
from typing import Optional

from fastapi import HTTPException
from hashids import Hashids

from data.database import SQLiteSession
from data.models import URL, USERS
from tinyurl.exception_handling import DataError
from tinyurl.logging import turl_logger


def create_user_record(user_name: str, email: str) -> bool:

    if not user_name or not email:
        raise ValueError("User name or email must not be none")

    db_session = SQLiteSession().connection_string
    one_user = USERS(Name=user_name, Email=email)
    db_session.add(one_user)
    db_session.commit()

    return True
