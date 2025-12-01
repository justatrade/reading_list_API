from fastapi import FastAPI
from src.routers.api.v1 import items_router, tags_router

app = FastAPI(docs_url="/swagger")

app.include_router(items_router)
app.include_router(tags_router)
