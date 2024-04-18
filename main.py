from fastapi import FastAPI
from jwt.auth import router

app = FastAPI()
app.include_router(router)