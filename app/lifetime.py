from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials
import sys
import os
from typing import Any


def register_startup_event(app: FastAPI) -> Any:
    # This will run on app startup
    # Initalizing firebase_admin with the realtime database credentials

    @app.on_event("startup")
    async def _startup() -> None:
        creds = credentials.Certificate(
            os.path.join(sys.path[0], r"app\credentials.json")
        )
        firebase_admin.initialize_app(
            creds,
            {
                "databaseURL": "https://financial-market-visualizer-default-rtdb.asia-southeast1.firebasedatabase.app/"
            },
        )

    return _startup
