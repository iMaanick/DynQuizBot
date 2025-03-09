from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from faststream.rabbit import fastapi
from starlette.middleware.cors import CORSMiddleware

from app.main.di import BrokerProvider, UseCaseProvider
from app.presentation.fastapi.root import root_router


def init_routers(app: FastAPI):
    app.include_router(root_router)
    router = fastapi.RabbitRouter("amqp://guest:guest@localhost:5672/")
    app.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_routers(app)
    container = make_async_container(BrokerProvider(), FastapiProvider(), UseCaseProvider())
    setup_dishka(container=container, app=app)
    return app
