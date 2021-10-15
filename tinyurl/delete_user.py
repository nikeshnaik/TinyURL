import random
from typing import Optional

from fastapi import HTTPException
from hashids import Hashids

from data.database import SessionLocal
from data.models import URL, USERS
from tinyurl.exception_handling import DataError
from tinyurl.logging import turl_logger


def delete_user_record(user_id: str, email: str) -> bool:

    if not user_id or not email:
        raise ValueError("User id or email must not be none")

    db_session = SessionLocal()
    record_deleted = (
        db_session.query(USERS)
        .filter(USERS.UserID == user_id, USERS.Email == email)
        .delete()
    )
    db_session.commit()

    return record_deleted
