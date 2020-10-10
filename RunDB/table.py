from .tools.path import PathType, PathTypeList, ensure_path, ensure_path_list, ensure_valide_name, ensure_json_file
from .tools.serialization import json_load, json_dump
from copy import deepcopy
from .recordset import RecordSet

class Table(RecordSet):
    def __init__(self, path: PathType, database=None, **kw):
        super(Table, self).__init__(table=self, **kw)
        self._db = database
        self._path = ensure_path(path)
        self._name = self._path.stem
        ensure_valide_name(self._name)
        self._load()
        

    # def One2many(self, table, keys=[]):
    #     return One2many(self, keys=keys)

    def _ensure_table(self):
        ensure_json_file(self._path)
    
    def dump(self):
        self._dump()

    def reload(self):
        self._load()

    def _dump(self):
        self._ensure_table()
        json_dump(self._path, self._data)
    
    def _load(self):
        self._ensure_table()
        data = json_load(self._path)
        self._data = data
