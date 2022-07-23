import os
from typing import Union, Literal

ROOT_FILES_FOLDER: Literal['./contents'] = "./contents"
AUTHORIZED: dict = {}
_users: str = os.getenv('users')
if _users is None: raise SyntaxError("Users to be authorized not found in env variables")
for user in _users.split(";"):
    u_p = user.split(":")
    AUTHORIZED[u_p[0]] = u_p[1]
