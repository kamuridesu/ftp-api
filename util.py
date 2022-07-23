import tempfile
import os


def generateFileRandomName(prefix="", suffix=""):
    return os.path.join(tempfile.gettempdir(), prefix + str(os.urandom(24).hex()) + suffix)
