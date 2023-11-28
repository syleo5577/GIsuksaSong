# from typing import Optional
# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel

# app = FastAPI()
# templates = Jinja2Templates(directory="./templates")

# # @app.get("/")
# # def master():
# #     return ""

# class Item(BaseModel):
#     code : int
#     name : str
#     real : Optional[bool] = None
    
# @app.get("/")
# def master(request : Request):
#     return templates.TemplateResponse("beta.html", {'request' : request})

# # @app.get("/items/{item_id}")
# # def read_item(item_id):
# #     return {"item_id": item_id}

# # @app.put("/items/{item_id}")
# # def update_item(item_id : int, name : Optional[str] = None):
# #     return {"item_id" : int, Item}

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}




# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True, workers=1)