from typing import Optional
from uuid import uuid1

from hashids import Hashids

from data.database import SQLiteSession
from data.models import URL, USERS

MIN_LENGTH = 8


def get_username_id(api_dev_key: str) -> USERS:

    db_session = SQLiteSession().connection_string
    record = db_session.query(USERS).filter(USERS.ApiDevKey == api_dev_key).all()
    if not record:
        raise ValueError("Api Dev Key Record not Found")

    return record[0]


def generate_short_key(api_dev_key: str, original_url: str) -> str:

    if not api_dev_key or not original_url:
        raise ValueError("Expected api_dev_key or Original URL to be not None")

    salt = api_dev_key + original_url

    hashid_obj = Hashids(salt=salt, min_length=MIN_LENGTH)

    user_object = get_username_id(api_dev_key=api_dev_key)

    unique_key = hashid_obj.encode(user_object.UserID)

    return unique_key


if __name__ == "__main__":

    api_dev_key = "1d5997a5-0d7d-41e3-8de6-73ea144183e6"
    ## check if username is unique in DB
    url = "https://www.educative.io/module/lesson/grokking-system-design-interview/xVZVrgDXYLP#4.-System-APIs"
    print(generate_short_key(api_dev_key=api_dev_key, original_url=url))
    print(generate_short_key(api_dev_key="", original_url=""))
