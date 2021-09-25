from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from pydantic import BaseModel, Field  # type: ignore

from tinyurl.keygen import generate_short_key

app = FastAPI()


class CreateUser(BaseModel):
    name: str
    email: str


class DeleteUser(BaseModel):
    user_id: int
    email: str


class CreateTinyURL(BaseModel):
    original_url: str
    api_dev_key: str
    expiry_date: Optional[datetime] = None


class DeleteURL(BaseModel):
    api_dev_key: str
    encoded_key: str


@app.post("/v1/encode-url")
def create_tinyurl(request: CreateTinyURL):
    print(request)
    ## encapsulate this inside a module and its database connection

    unique_key = generate_short_key(request.api_dev_key, request.original_url)
    # ToDo: Dump it to DB.
    return unique_key


@app.delete("/v1/delete-url")
def delete_url(request: DeleteURL):
    print(request)
    ## seperate module
    return {"Confirmed": False}


@app.post("/v1/create-user")
def create_user(request: CreateUser):
    print(request)
    ## seperate module
    return {"Confirmed": request}


@app.post("/v1/delete-user")
def delete_user(request: DeleteUser):
    print(request)
    ## seperate module
    return {"Confirmed": request}


@app.get("/{shortkey}")
def read_tinyurl(shortkey: str):
    print(shortkey)
    ## seperate module
    ##ToDo
    return {"Confirmed": "Redirecting to original link"}
