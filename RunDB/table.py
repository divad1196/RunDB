from .tools.path import PathType, PathTypeList, ensure_path, ensure_path_list, ensure_valide_name, ensure_json_file
from .tools.serialization import json_load, json_dump, default_anonymous_key, default_serializer, default_deserializer
from typing import Callable, Optional
from .relational import One2many

class Table:
    def __init__(
        self,
        path: PathType,
        autodump:bool = False,
        serializer: Callable=default_serializer,
        deserializer: Callable=default_deserializer,
        anonymous: Callable=default_anonymous_key
    ):
        self._path = ensure_path(path)
        self._name = self._path.stem
        ensure_valide_name(self._name)
        self._data = []
        self._load()
        self._autodump = autodump
        self.set_serializer(serializer)
        self.set_deserializer(deserializer)
        self._anonymous_key = anonymous

    def One2many(self, table, keys=[]):
        return One2many(self, keys=keys)
        
    def update_config(self, **kwargs):
        autodump = kwargs.get("autodump")

        if autodump:
            self._autodump = autodump
        serializer = kwargs.get("serializer")

        if serializer:
            self._serializer = serializer
        deserializer = kwargs.get("deserializer")

        if deserializer:
            self._deserializer = deserializer
        anonymous = kwargs.get("anonymous")

        if anonymous:
            self._anonymous_key = anonymous

    def set_serializer(self, func: Callable):
        self._serializer = func

    def set_deserializer(self, func: Callable):
        self._deserializer = func

    def _ensure_table(self):
        ensure_json_file(self._path)
    
    def force_dump(self):
        self._dump()

    def reload(self):
        self._load()

    def append(self, data):
        self[self._anonymous_key(data)] = data

    def _dump(self):
        self._ensure_table()
        json_dump(self._path, self._data)
    
    def _load(self):
        self._ensure_table()
        data = json_load(self._path)
        self._data = data

    def __bool__(self):
        return bool(self._data)

    def __str__(self):
        return self._name
    
    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return self._deserializer(self._data[key])

    def __setitem__(self, key, item):
        self._data[key] = self._serializer(item)
        if self._autodump:
            self._dump()

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def get(self, key, default=None):
        data = self._data.get(key)
        if data:
            return self._deserializer(data)
        return default

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def update(self, condition: Optional[Callable] = None, kwargs: dict = {}):
        data = self.filter(condition)
        for d in data:
            if isinstance(d, dict):
                d.update(kwargs)

    def filter(self, condition: Optional[Callable] = None):
        data = {}
        if condition is None:
            condition = bool
        for key, value in self.items():
            if condition(value):
                data[key] = value
        return data

    def filter_values(self, condition: Optional[Callable] = None):
        return filter(condition, self.values())
    
    def update_key(self, old_key, new_key):
        self._data[new_key] = self._data
