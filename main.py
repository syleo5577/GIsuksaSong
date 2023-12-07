from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from pydantic import BaseModel
import db_functions as db
import link_functions as link


app = FastAPI()
app.mount(
    "/templates",
    StaticFiles(directory="../GisuksaSong/templates"),
    name="templates"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 도메인들
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메소드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)


class linkInput(BaseModel):
    url: str


class DataStorage(BaseModel):
    data: list[list]


@app.get("/")
async def blank():
    return "터프가이김성민!"


@app.get("/list")
async def root():
    return FileResponse("templates/main.html")


@app.get("/list/data")
async def getData(gen: int):
    data = db.getDataWithoutDeleted(gen)
    return {"arr": data}


@app.get("/list/download")
async def getVideo(gen: int, index: int, code: str):
    dir = await db.downloadVideo(code)
    if os.path.isfile(dir):
        db.deactivate(gen, index)
        return FileResponse(dir, headers={"result": 'success'})
    else:
        return {"error": dir, "result": 'runtime error'}


@app.get("/list/delete")
async def deleteItem(gen: int, index: int, code: str):
    result = db.delete(gen, index)
    return {'result': result, 'location': 'delete'}


@app.get("/list/ban")
async def banItem(gen: int, index: int, code: str):
    result = db.ban(gen, index, code)
    if result == 'success':
        db.delete(gen, index)
    return {'result': result, 'loaction': 'ban'}


@app.post("/list")
async def post_url(gen: int, item: linkInput):
    # print(url)
    url = link.addHTTPS(item.url)
    url = item.url
    # print(url)
    code = link.getYoutubeVideoID(url)
    # print(code)
    if code:
        print("code:", code)
        r, appendVideoData = db.dbAppend(gen, code)
        if r == "success":
            return {
                "result": r,
                "index": appendVideoData[0],
                "code": appendVideoData[1],
                "title": appendVideoData[2],
                "unixtime": appendVideoData[4]
            }
        return {"result": r}
    else:
        print("NOT YOUTUBE VIDEO")
        return {"result": "not video"}
    