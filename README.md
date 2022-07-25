# FTP-API
This is a really simple ftp api written in Python3 with FastAPI.

## Purpose
The purpose of this is to deliver a fast do deploy, minimal FTP api on servers.

## Usage
While the image is not on Docker Hub yet, you'll need to build it yourself:
```sh
docker build -t ftp-api .
```
### Running
To run it, you'll need to attach a volume to the container specifying the /app/contents folder as well the users that have access using env vars:
```sh
docker run -d --name ftp-api -p 80:8000 -e users="kamuri:123;test:user" -v $(pwd)/contents:/app/contents ftp-api
```
