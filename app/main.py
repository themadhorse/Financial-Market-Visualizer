from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from app.exception_handlers import default_error_handler
import firebase_admin
from firebase_admin import credentials
import os
import sys


app = FastAPI()

origins = ["http://localhost", "http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Adding startup event
# register_startup_event(app)
creds = credentials.Certificate(os.path.join(sys.path[0], r"app\credentials.json"))
firebase_admin.initialize_app(
    creds,
    {
        "databaseURL": "https://financial-market-visualizer-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)

# All routers that require firebase setup must be imported after the above startup event
from app.routers import users  # noqa: E402


# Adding high level exception handler for all generic exceptions
app.add_exception_handler(Exception, default_error_handler)

# Adding all the APIRouters
app.include_router(users.router)


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}
