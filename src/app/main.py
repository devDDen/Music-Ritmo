import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db_endpoints import router
from .open_subsonic_api import open_subsonic_router
from .db_loading import scan_and_load
from .frontend_endpoints import frontend_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scan_and_load()

app.include_router(router)

app.include_router(open_subsonic_router)

app.include_router(frontend_router)
