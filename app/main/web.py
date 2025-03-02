from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routers import init_routers


def create_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_routers(app)
    return app