from fastapi import FastAPI

from src.routers.api.v1 import (
    admin_router,
    items_router,
    tags_router,
    users_router,
)

app = FastAPI(docs_url="/swagger")


app.include_router(admin_router)
app.include_router(items_router)
app.include_router(tags_router)
app.include_router(users_router)
