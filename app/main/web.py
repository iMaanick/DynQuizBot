from fastapi import FastAPI
from faststream.rabbit import fastapi
from starlette.middleware.cors import CORSMiddleware

from app.presentation.fastapi.root import root_router


def init_routers(app: FastAPI):
    app.include_router(root_router)
    router = fastapi.RabbitRouter("amqp://guest:guest@localhost:5672/")
    app.include_router(router)


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
