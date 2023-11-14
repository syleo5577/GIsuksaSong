from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    code : int
    name : str
    real : Optional[bool] = None
    

@app.get("/")
def master():
    return "Hello, world!"

@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}

@app.put("/items/{item_id}")
def update_item(item_id : int, name : Optional[str] = None):
    return {"item_id" : int, Item}