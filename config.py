import os
from typing import Union, Literal

ROOT_FILES_FOLDER = "./contents"
AUTHORIZED: dict = {}
_users: Union[str, None] = os.getenv('users')
# if _users is None: raise SyntaxError("Users to be authorized not found in env variables")
if _users is None: _users="kamuri:123"
for user in _users.split(";"):
    user_and_password = user.split(":")
    AUTHORIZED[user_and_password[0]] = user_and_password[1]
