from typing import Union
from api.router import user_router

from fastapi import FastAPI

app = FastAPI()


app.include_router(user_router.router, prefix="/user", tags=["Users"])

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}