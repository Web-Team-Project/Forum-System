from fastapi import FastAPI
from routers.auth import auth_router
from routers.topics import topics_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(topics_router)