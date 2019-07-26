from os import environ, pathsep
from pathlib import Path
from .utils import Util

for path in environ["PATH"].split(pathsep):
    for util in Path(path).glob("*"):
        globals()[util.name] = Util(util.name)
