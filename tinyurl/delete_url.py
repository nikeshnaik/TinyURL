import random
from typing import Optional

from data.database import SQLiteSession
from data.models import URL, USERS
from tinyurl.exception_handling import DataError
from tinyurl.logging import turl_logger


def delete_encoded_url(api_dev_key: str, encoded_url: str) -> bool:

    if not api_dev_key or not encoded_url:
        raise DataError(detail="Expected api_dev_key or encoded URL to be not None")
    db_session = SQLiteSession().connection_string
    user_object = db_session.query(USERS).filter(USERS.ApiDevKey == api_dev_key).one()

    record_deleted = (
        db_session.query(URL)
        .filter(URL.UserID == user_object.UserID, URL.EncodedURL == encoded_url)
        .delete()
    )
    db_session.commit()

    return record_deleted
