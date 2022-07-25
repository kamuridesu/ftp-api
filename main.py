import secrets
from zipfile import ZipFile
import shutil

from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.background import BackgroundTasks

from config import *
from util import *

app = FastAPI()
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    username: Union[str, None] = None
    for user in AUTHORIZED.keys():
        if secrets.compare_digest(credentials.username, user):
            username = user
            break
    is_valid_password = None
    if username is not None:
        is_valid_password = secrets.compare_digest(credentials.password, AUTHORIZED[username])
    if not (username is not None and is_valid_password):
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
async def error(message: str="Generic error", code: int=400):
    print("An error occured!")
    raise HTTPException(
        status_code=int(code),
        detail=message
    )


@app.get("/files/{filename}")
async def getFile(filename: Union[str, int], is_valid_user: str = Depends(get_current_username)):
    if is_valid_user:
        files = os.listdir(ROOT_FILES_FOLDER)
        try:
            filename = int(filename)
        except (TypeError, ValueError):
            pass
        if isinstance(filename, str):
            if filename in files:
                if not os.path.isfile(filename):
                    filename = os.path.join(ROOT_FILES_FOLDER, filename)
                    if not os.path.isfile(filename):
                        return RedirectResponse("/error?message=File not found&code=404")
                return FileResponse(filename)
        elif isinstance(filename, int) and filename < len(files):
            try:
                return FileResponse(os.path.join(ROOT_FILES_FOLDER, files[filename]))
            except Exception as e:
                pass
        return RedirectResponse("/error?message=File not found&code=404")


@app.get("/files/all")
async def getAllZip(bg_tasks: BackgroundTasks, is_valid_user: str = Depends(get_current_username)):
    if is_valid_user:
        temp_name = generateFileRandomName(suffix=".zip")
        with ZipFile(temp_name, "w") as _zip:
            for file in os.listdir(ROOT_FILES_FOLDER):
                filepath = os.path.join(ROOT_FILES_FOLDER, file)
                _zip.write(filepath)
        bg_tasks.add_task(os.remove, temp_name)
        return FileResponse(temp_name, background=bg_tasks)


@app.get("/health")
async def healthcheck():
    total, used, free = shutil.disk_usage("/")
    return {
        "status": "ok",
        "disk": {
            "total": total,
            "used": used,
            "free": free
        }
    }


@app.get("/")
async def index():
    return {
        "endpoints": [
            "/files",
            "/files/{filename|id}",
            "/files/all",
            "health"
        ]
    }
