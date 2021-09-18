from random import randint
from typing import Optional

from hashids import Hashids

MIN_LENGTH = 8


def get_username_id(username: str) -> int:

    ## Sql to get id and return
    ## id are actually primarykey of table. max it go to 7 billion

    return randint(1, 100)


def generate_short_key(username: str, original_url: str) -> str:

    if not username or not original_url:
        raise ValueError("Expected Username or Original URL to be not None")

    salt = username + original_url

    hashid_obj = Hashids(salt=salt, min_length=MIN_LENGTH)

    primary_key = get_username_id(username=username)
    unique_key = hashid_obj.encode(primary_key)

    return unique_key


if __name__ == "__main__":

    username = "nikeshnaik"
    ## check if username is unique in DB
    url = "https://www.educative.io/module/lesson/grokking-system-design-interview/xVZVrgDXYLP#4.-System-APIs"
    print(generate_short_key(username=username, original_url=url))
    print(generate_short_key(username="", original_url=""))
