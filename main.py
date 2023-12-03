from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles 
import os
from pydantic import BaseModel
import db_functions as db
import link_functions as link


app = FastAPI()
app.mount("/templates", StaticFiles(directory="../GisuksaSong/templates"), name="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 도메인들
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메소드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)


# templates = Jinja2Templates(directory="templates")


class linkInput(BaseModel):
    url: str

class DataStorage(BaseModel):
    data: list[list]


@app.get("/")
async def blank():
    return "Hello, world!"

# @app.get("/list")
# async def root(request: Request):
    # return templates.TemplateResponse("main.html", {"request": request})

@app.get("/list")
async def root():
    return FileResponse("templates/main.html")

@app.get("/list/data")
async def get_item(gen : int):
    print("asdf")
    data = db.getDataWithoutDeleted(gen)
    return {"arr": data}  # 저장된 데이터 반환

@app.get("/list/audio")
async def get_audio(gen : int, index : int):
    path = await db.downloadVideo(gen, index)
    db.deactivate(gen, index)
    return FileResponse(path, filename=f"{os.path.basename(path)}")

@app.get("/list/deactivate")
async def deleteItem(gen : int, index : int):
    # r = db.deactivate(gen, index)
    # if r == 0:
    #     return {"result": "success"}
    # else:
    #     return {"result": "runtime error"}
    print("deactivate:", gen, index)
    return {"messege": "deactivate"}

@app.get("/list/delete")
async def deleteItem(gen : int, index : int):
    # r = db.delete(gen, index)
    # if r == 0:
    #     return {"result": "success"}
    # else:
    #     return {"result": "runtime error"}
    print("delete:", gen, index)
    return {"messege": "delete"}

@app.get("/list/ban")
async def deleteItem(gen : int, index : int):
    # arr = db.getData(gen)
    # code = arr[index][2]
    
    # r = db.ban(gen, code)
    # if r == 0:
    #     return {"result": "success"}
    # elif r == 2:
    #     return {"result": "duplicated"}
    # else:
    #     return {"result": "runtime error"}
    print("ban:", gen, index)
    return {"messege": "ban"}

@app.post("/list")
async def post_url(gen : int, item : linkInput):
    # print(url)
    url = link.addHTTPS(item.url)
    url = item.url
    # print(url)
    code = link.getYoutubeVideoID(url)
    # print(code)
    if code:
        print("code:", code)
        r = db.dbAppend(gen, code)
        return {"result": r}
    else:
        print("NOT YOUTUBE VIDEO")
        return {"result": "not youtube video"}
    # print(item)
    # return {"messege": "asdf"}