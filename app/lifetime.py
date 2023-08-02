from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials
from typing import Awaitable, Callable
import sys
import os


def register_startup_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    # This will run on app startup, initalizing firebase_admin with the realtime database credentials
    
    @app.on_event('startup')
    async def _startup() -> None:
        creds = credentials.Certificate(os.path.join(sys.path[0], 'app\credentials.json'))
        firebase_admin.initialize_app(credential=creds)
    return _startup