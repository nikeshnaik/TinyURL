import random
from typing import Optional

from fastapi import HTTPException
from hashids import Hashids

from data.database import SQLiteSession
from data.models import URL, USERS
from tinyurl.exception_handling import DataError
from tinyurl.logging import turl_logger

MIN_LENGTH = 8


def get_username_id(api_dev_key: str) -> USERS:

    db_session = SQLiteSession().connection_string
    record = db_session.query(USERS).filter(api_dev_key == api_dev_key).all()
    db_session.close()
    if not record:
        raise DataError(detail="Api Dev Key Not found")

    return record[0]


def dump_to_database(user_id: str, unique_key: str, original_url: str) -> bool:

    db_session = SQLiteSession().connection_string
    one_url = URL(EncodedURL=unique_key, OriginalURL=original_url, UserID=user_id)
    db_session.add(one_url)
    db_session.commit()

    return True


def generate_short_key(api_dev_key: str, original_url: str) -> str:
    print(api_dev_key, original_url)
    if not api_dev_key or not original_url:
        raise DataError(detail="Expected api_dev_key or Original URL to be not None")

    salt = api_dev_key + str(random.randint(1, 100000000))
    print(salt)

    hashid_object = Hashids(salt=salt, min_length=MIN_LENGTH)

    user_object = get_username_id(api_dev_key=api_dev_key)

    unique_key = hashid_object.encode(user_object.UserID)
    print(unique_key)

    dump_to_db = dump_to_database(user_object.UserID, unique_key, original_url)

    return unique_key


if __name__ == "__main__":

    api_dev_key = "1d5997a5-0d7d-41e3-8de6-73ea144183e6"
    ## check if username is unique in DB
    url = "https://www.educative.io/module/lesson/grokking-system-design-interview/xVZVrgDXYLP#4.-System-APIs"
    print(generate_short_key(api_dev_key=api_dev_key, original_url=url))
    print(generate_short_key(api_dev_key="", original_url=""))
