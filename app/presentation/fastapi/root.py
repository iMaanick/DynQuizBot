from fastapi import APIRouter

from .index import index_router

root_router = APIRouter()

root_router.include_router(
    index_router,
)
