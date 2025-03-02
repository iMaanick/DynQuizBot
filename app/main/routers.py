from fastapi import FastAPI
from faststream.rabbit import fastapi

from app.presentation.fastapi.root import root_router


def init_routers(app: FastAPI):
    app.include_router(root_router)
    router = fastapi.RabbitRouter("amqp://guest:guest@localhost:5672/")
    app.include_router(router)
