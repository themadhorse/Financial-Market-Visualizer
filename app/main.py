from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from app.exception_handlers import default_error_handler
from app.lifetime import register_startup_event

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
register_startup_event(app)

# Adding high level exception handler for all generic exceptions
app.add_exception_handler(Exception, default_error_handler)


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}
