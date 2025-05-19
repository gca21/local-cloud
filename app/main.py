from fastapi import FastAPI
from app.api import root, items

app = FastAPI()

app.include_router(root.router)
app.include_router(items.router)
