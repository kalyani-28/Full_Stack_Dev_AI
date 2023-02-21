import os
import io
import shutil
import zipfile

from fastapi import Depends, FastAPI, Form, Request, Response, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse

from apiGenerator.apiGenerator import generateApi
from textbox_label.textbox_label import getTextbox_Labels

from imageProcessEngine import imageProcess

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "../gcp-auth.json"


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/404")


@app.get("/", response_class=HTMLResponse)
def main():
    return FileResponse("pages/frontEnd.html")


@app.post("/generateApp")
async def main(file: UploadFile):
    src = os.path.abspath("../results/source.png")
    with open(src, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # data = await file.read()
    # coords = getTextbox_Labels(data)
    # labels = [l[4] for l in sorted(coords, key=lambda x: x[1])]
    # formElements = {k: {"label": l, "type": "text"}
    #                 for k, l in enumerate(labels)}
    # generateApi([formElements])
    img = imageProcess.run(src)

    generateApi([img.mapping])

    zipFilename = "app.zip"
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")

    appPath = os.path.abspath("../results/webApp")
    for root, _, files in os.walk(appPath):
        for f in files:
            fPath = os.path.join(root, f)
            zf.write(fPath, os.path.relpath(fPath, appPath))

    zf.close()
    shutil.rmtree(appPath)

    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        "Content-Disposition": f"attachment;filename={zipFilename}"
    })

    return resp


@app.get("/404")
async def main():
    return FileResponse("pages/404.html")
