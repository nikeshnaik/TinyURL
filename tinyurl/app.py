from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import uvicorn
from dateutil.relativedelta import relativedelta
from fastapi import Depends, FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field  # type: ignore

from tinyurl.exception_handling import ExceptionRoute
from tinyurl.keygen import generate_short_key
from tinyurl.logging import turl_logger

app = FastAPI()
router = APIRouter(route_class=ExceptionRoute)


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


@router.post("/v1/encode-url")
def create_tinyurl(request: CreateTinyURL):
    # try:
    unique_key = generate_short_key(request.api_dev_key, request.original_url)
    turl_logger.info(
        msg="Request Processed", extra={**request.dict(), "response_code": 200}
    )
    # except AppError as e:
    #     turl_logger.error(msg=e.detail, extra={**request.dict(), "response_code":e.status_code})
    #     raise

    return unique_key


@router.delete("/v1/delete-url")
def delete_url(request: DeleteURL):
    print(request)
    ## seperate module
    return {"Confirmed": False}


@router.post("/v1/create-user")
def create_user(request: CreateUser):
    print(request)
    ## seperate module
    return {"Confirmed": request}


@router.post("/v1/delete-user")
def delete_user(request: DeleteUser):
    print(request)
    ## seperate module
    return {"Confirmed": request}


@router.get("/{shortkey}")
def read_tinyurl(shortkey: str):
    print(shortkey)
    ## seperate module
    ##ToDo
    return {"Confirmed": "Redirecting to original link"}


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=5000, debug=True, reload=False, log_level="info"
    )
