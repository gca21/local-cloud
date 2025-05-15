from fastapi import FastAPI
from app.api import root

app = FastAPI()

app.include_router(root.router)
