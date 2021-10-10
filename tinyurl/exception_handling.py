from typing import Callable

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute

from tinyurl.logging import turl_logger


### Always raise one of these errors inside code
class DataError(HTTPException):
    def __init__(
        self, status_code: int = 404, detail="Data not Found", headers=None
    ) -> None:
        ## If needed add headers here as well
        super().__init__(status_code, detail=detail, headers=headers)


### Handling Exception at global level in fastapi triggers Starlette Exception which doesn't give correct exception class, workaround by fastpapi devs
# https://github.com/tiangolo/fastapi/issues/2750#issuecomment-775526951


class ExceptionRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            try:
                response: Response = await original_route_handler(request)
                return response
            except Exception as err:
                if isinstance(err, DataError):
                    turl_logger.error(
                        msg=err.detail,
                        stack_info=True,
                        extra={"response_code": err.status_code},
                    )
                    return JSONResponse(
                        content="Data Error: " + err.detail, status_code=err.status_code
                    )
                ## Add if any specific exception class needed.
                else:
                    turl_logger.error(
                        msg=str(err), stack_info=True, extra={"response_code": 500}
                    )
                    return JSONResponse(
                        content="Internal Server Error", status_code=500
                    )

        return custom_route_handler
