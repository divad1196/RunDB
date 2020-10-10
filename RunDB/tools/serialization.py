
from typing import Union, List, Iterable, Callable
import json
import inspect
from uuid import uuid4

def func_keys(func):
    signature = inspect.signature(func)
    filter_keys = [
        param.name
        for param in signature.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD
    ]
    return filter_keys

def filter_dict(kwargs, keys):
    filtered_dict = {
        k: kwargs[k]
        for k in keys
        if k in kwargs
    }
    return filtered_dict

def call_kwargs(func, kwargs):
    keys = func_keys(func)
    params = filter_dict(kwargs, keys)
    return func(**params)

def json_load(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def json_dump(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

def is_jsonable(obj):
    try:
        json.dumps(obj)
        return True
    except Exception:
        return False

def get_random_id():
    return str(uuid4())