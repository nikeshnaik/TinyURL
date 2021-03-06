import os
import pathlib
from datetime import datetime
from pathlib import Path
from sys import prefix
from typing import Optional
from uuid import UUID, uuid4

import uvicorn
from dateutil.relativedelta import relativedelta
from fastapi import Depends, FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field  # type: ignore
from pydantic.types import Json
from starlette.responses import FileResponse

from data.models import Base, insert_data
from tinyurl.create_user import create_user_record
from tinyurl.delete_url import delete_encoded_url
from tinyurl.delete_user import delete_user_record
from tinyurl.exception_handling import ExceptionRoute
from tinyurl.get_api_dev_key import get_user_apidevkey
from tinyurl.key_redirect import get_original_url
from tinyurl.keygen import generate_short_key
from tinyurl.logging import turl_logger

app = FastAPI()

Base_dir = Path(__name__).resolve().parent
origins = [
    "https://cloned-link.com",
    "https://www.cloned-link.com",
    "https://api.cloned-link.com",
    "https://app.cloned-link.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


router = APIRouter()


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


@router.post("/encode-url")
def create_tinyurl(request: CreateTinyURL):
    unique_key = generate_short_key(request.api_dev_key, request.original_url)
    turl_logger.info(
        msg="Request Processed", extra={**request.dict(), "response_code": 200}
    )

    return {"msg": unique_key}


@router.delete("/delete-url")
def delete_url(request: DeleteURL):
    record_deleted = delete_encoded_url(request.api_dev_key, request.encoded_key)
    turl_logger.info(
        msg="Request Processed", extra={**request.dict(), "response_code": 200}
    )
    return {"msg": f"Resource Deleted {record_deleted}"}


@router.post("/create-user")
def create_user(request: CreateUser):
    user_record_created = create_user_record(request.user_name, request.email)
    user_api_dev_key = get_user_apidevkey(request.user_name, request.email)
    turl_logger.info(
        msg="Request Processed", extra={**request.dict(), "response_code": 200}
    )

    return {
        "msg": f"Resource Created {user_record_created} and user api_dev_key is {user_api_dev_key}"
    }


@router.delete("/delete-user")
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

    return RedirectResponse(original_url)


app.include_router(router)

print([{"path": route.path, "name": route.name} for route in app.routes])


if __name__ == "__main__":

    uvicorn.run(
        app, host="0.0.0.0", port=5000, debug=True, reload=False, log_level="info"
    )
