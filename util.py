import tempfile
import os
import json
from typing import Any


def generateFileRandomName(prefix="", suffix=""):
    return os.path.join(tempfile.gettempdir(), prefix + str(os.urandom(24).hex()) + suffix)


def getLengthRecursive(dictionary):
    length = 0
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            length += getLengthRecursive(dictionary[key])
        elif isinstance(dictionary[key], list):
            length += len(dictionary[key])
    return length


def generateJsonFromPath(path, json_content: dict[str, list]={}, id=0):
    if os.path.isdir(path):
        path_basename = os.path.basename(path)
        if path_basename == "contents":
            path_basename = "."
        json_content[path_basename] = []
        for file in os.listdir(path):
            filepath = os.path.join(path, file)
            if os.path.isfile(filepath):
                json_content[path_basename].append({
                    "id": id,
                    "name": file
                })
            else:
                generateJsonFromPath(filepath, json_content, id + 1)
    return {
        "total_files": getLengthRecursive(json_content),
        "files": json_content
    }


def findFilesById(path, id):
    files = generateJsonFromPath(path)
    for key, value in files["files"].items():
        for value in value:
            if value["id"] == id:
                return os.path.join(key, value["name"])
