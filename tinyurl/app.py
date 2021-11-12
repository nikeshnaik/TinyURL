import os
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic.types import Json

import uvicorn
from dateutil.relativedelta import relativedelta
from fastapi import Depends, FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field  # type: ignore

from data.models import Base, insert_data
from tinyurl.create_user import create_user_record
from tinyurl.delete_url import delete_encoded_url
from tinyurl.delete_user import delete_user_record
from tinyurl.exception_handling import ExceptionRoute
from tinyurl.get_api_dev_key import get_user_apidevkey
from tinyurl.key_redirect import get_original_url
from tinyurl.keygen import generate_short_key
from tinyurl.logging import turl_logger

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

Base_dir = Path(__name__).resolve().parent

app.mount("/", StaticFiles(directory=Path(Base_dir,"./frontend"), html=True), name="static")

# origins = [
#         "https://cloned-link.com/",
#         "http://cloned-link.com",
#         "http://localhost",
#         "http://localhost:8080",
#         "http://127.0.0.1:5000", 
#         "http://127.0.0.1:5000/"

#         ]

# app.add_middleware(
#         CORSMiddleware,
#         allow_origins=origins,
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"]
#         )


router = APIRouter(route_class=ExceptionRoute)


class CreateUser(BaseModel):
    user_name: str
    email: str


class DeleteUser(BaseModel):
    user_id: str
    email: str


class CreateTinyURL(BaseModel):
    original_url: str
    api_dev_key: str
    expiry_date: Optional[datetime] = None


class DeleteURL(BaseModel):
    api_dev_key: str
    encoded_key: str


@router.post("/v1/encode-url")
def create_tinyurl(request: CreateTinyURL):
    unique_key = generate_short_key(request.api_dev_key, request.original_url)
    turl_logger.info(
        msg="Request Processed", extra={**request.dict(), "response_code": 200}
    )

    response = JSONResponse(content={"msg": unique_key}, headers={"Content-Type": "application/json"})

    return response


@router.delete("/v1/delete-url")
def delete_url(request: DeleteURL):
    record_deleted = delete_encoded_url(request.api_dev_key, request.encoded_key)
    turl_logger.info(
        msg="Request Processed", extra={**request.dict(), "response_code": 200}
    )
    return {"msg": f"Resource Deleted {record_deleted}"}


@router.post("/v1/create-user")
def create_user(request: CreateUser):
    user_record_created = create_user_record(request.user_name, request.email)
    user_api_dev_key = get_user_apidevkey(request.user_name, request.email)
    turl_logger.info(
        msg="Request Processed", extra={**request.dict(), "response_code": 200}
    )

    return {
        "msg": f"Resource Created {user_record_created} and user api_dev_key is {user_api_dev_key}"
    }


@router.delete("/v1/delete-user")
def delete_user(request: DeleteUser):
    record_deleted = delete_user_record(request.user_id, request.email)
    turl_logger.info(
        msg="Request Processed", extra={**request.dict(), "response_code": 200}
    )

    return {"msg": f"Resource Deleted {record_deleted}"}


@router.get("/{shortkey}")
def read_tinyurl(shortkey: str):
    original_url = get_original_url(shortkey)
    turl_logger.info(
        msg=f"Redirected to original url {original_url}",
        extra={"short_key": shortkey, "response_code": 200},
    )
    # html = f"<script>window.location.replace({original_url})</script>"
    html = f"<head><meta http-equiv='Refresh' content='0; URL={original_url}'></head>"


    return RedirectResponse(original_url)


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=5000, debug=True, reload=False, log_level="info"
    )
