import re
from pathlib import Path
from uuid import uuid4
from typing import Union, List, Iterable, Callable
from .serialization import json_dump

PathType = Union[Path, str]
PathTypeList = Union[PathType, Iterable[PathType]]

REG_NAME_VALIDATION = re.compile("[a-z]|[_-]")

def is_name_valide(name):
    return bool(REG_NAME_VALIDATION.match(name))

def ensure_valide_name(name):
    if not is_name_valide(name):
        raise Exception("Name '{name}' is not valide".format(
            name=name,
        ))

def json_ext(name):
    return name + ".json"

def ensure_path(path: PathType):
    return Path(path).resolve()

def ensure_path_list(paths: PathTypeList):
    if not isinstance(paths, List):
        if isinstance(paths, Iterable):
            paths = list(paths)
        else:
            paths = [paths]
    paths = [ensure_path(p) for p in paths]
    return paths

def ensure_dir(path: PathType):
    path = ensure_path(path)
    path.mkdir(parents=True, exist_ok=True)

def ensure_file(path: PathType):
    path = ensure_path(path)
    if path.is_file():
        return
    elif path.exists():
        raise Exception("file {path} exists but is not a file".format(
            path=path
        ))
    ensure_dir(path.parent)
    path.open('x').close()

def ensure_json_file(path: PathType):
    path = ensure_path(path)
    if path.is_file():
        return
    elif path.exists():
        raise Exception("file {path} exists but is not a file".format(
            path=path
        ))
    ensure_dir(path.parent)
    json_dump(path, {})