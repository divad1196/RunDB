
from typing import Union, List, Iterable, Callable
import json

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

def default_serializer(obj):
    return obj

def default_deserializer(obj):
    return obj

def get_random_id():
    return str(uuid4())

def default_anonymous_key(obj):
    return get_random_id()