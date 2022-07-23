from typing import Union
import json
import secrets
from zipfile import ZipFile
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.background import BackgroundTasks
from config import *
from util import *

app = FastAPI()
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    usernamme: Union[str, None] = None
    for user in AUTHORIZED.keys():
        if secrets.compare_digest(credentials.username, user):
            username = user
            break
    is_valid_password = secrets.compare_digest(credentials.password, AUTHORIZED[username])
    if not (usernamme is None and is_valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


@app.get("/files")
async def getFiles(is_valid_user: str = Depends(get_current_username)):
    if is_valid_user:
        files = os.listdir(ROOT_FILES_FOLDER)
        return {
            "total_files": len(files),
            "files": files
        }


@app.get("/error", status_code=400)
async def error(response: Response, message: str="Generic error", code: int=400):
    print("An error occured!")
    response.status_code = int(code)
    return {
        "mesage": message
    }


@app.get("/file/{filename}")
async def getFile(filename: str, is_valid_user: str = Depends(get_current_username)):
    if is_valid_user:
        files = os.listdir(ROOT_FILES_FOLDER)
        if filename in files:
            if not os.path.isfile(filename):
                filename = os.path.join(ROOT_FILES_FOLDER, filename)
                if not os.path.isfile(filename):
                    return RedirectResponse("/error?message=File not found&code=404")
            with open(filename, "r", encoding="utf-8") as f:
                return json.loads(f.read())
        return RedirectResponse("/error?message=File not found&code=404")


@app.get("/all")
async def getAllZip(bg_tasks: BackgroundTasks, is_valid_user: str = Depends(get_current_username)):
    if is_valid_user:
        temp_name = generateFileRandomName(suffix=".zip")
        with ZipFile(temp_name, "w") as _zip:
            for file in os.listdir(ROOT_FILES_FOLDER):
                filepath = os.path.join(ROOT_FILES_FOLDER, file)
                _zip.write(filepath)
        bg_tasks.add_task(os.remove, temp_name)
        return FileResponse(temp_name, background=bg_tasks)
