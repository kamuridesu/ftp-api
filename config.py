import os
from typing import Union
import sys

ROOT_FILES_FOLDER = "./contents"
AUTHORIZED: dict = {}
_users: Union[str, None] = os.getenv('users')
if "--debug" in sys.argv: _users = "admin:123"
if _users is None: raise SyntaxError("Users to be authorized not found in env variables")
for user in _users.split(";"):
    user_and_password = user.split(":")
    AUTHORIZED[user_and_password[0]] = user_and_password[1]
