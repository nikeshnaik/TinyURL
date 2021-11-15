from os import name
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from data.models import Base
app = FastAPI(docs_url=None, redoc_url=None)

Base_dir = Path(__name__).resolve().parent
origins = [
    "https://www.cloned-link.com/",
    "https://app.cloned-link.com/"
    # "http://cloned-link.com",
    # "http://localhost",
    # "http://localhost:8080",
    # "http://127.0.0.1:5000",
    # "http://127.0.0.1:5000/"
    # "*"
]

app.mount("/", StaticFiles(directory=Base_dir / "frontend", html=True), name="static")

if __name__ == "__main__":

    uvicorn.run(
        app, host="0.0.0.0", port=8000, debug=True, reload=False, log_level="info"
    )
