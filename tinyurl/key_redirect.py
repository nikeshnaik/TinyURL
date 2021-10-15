import random
from typing import Optional

from fastapi import HTTPException
from hashids import Hashids

from data.database import SessionLocal
from data.models import URL, USERS
from tinyurl.exception_handling import DataError
from tinyurl.logging import turl_logger


def get_original_url(short_key: str) -> str:

    if not short_key:
        raise ValueError("Url must not be None")

    db_session = SessionLocal()
    url_record = db_session.query(URL).filter(URL.EncodedURL == short_key).one()
    db_session.close()

    if not url_record:
        raise DataError(status_code=404, detail="Encoded URL not Found")

    return url_record.OriginalURL
