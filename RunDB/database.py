from .tools.path import PathType, PathTypeList, ensure_path, ensure_path_list, ensure_valide_name, ensure_dir, json_ext
from .table import Table
import os

# Store DB informations into a json file?

class Database:
    def __init__(self, database: PathType):
        db_path = ensure_path(database)
        self._path = db_path
        self._tables = {}
        # self._load()  # conflicts with table definitions

    def list_tables(self):
        return list(self.keys())

    def table(self, name, **kw):
        return self.get_or_create_table(name, **kw)

    def register(self, key, table: Table):
        if key in self._tables:
            raise Exception("A table is already register under key '{key}'".format(
                key=key
            ))
        self._tables[key] = table

    def get_or_create_table(self, name, **kw):
        ensure_valide_name(name)
        table = self._tables.get(name)
        if table is not None:
            return table
        return self._create_table(name, **kw)

    def _create_table(self, name, **kwargs):
        ensure_valide_name(name)
        if name in self._tables:
            raise Exception("Table {name} already exists".format(
                name=name,
            ))
        self._ensure_database()
        filename = json_ext(name)
        table_path = self._path.joinpath(filename)

        kwargs.pop("path", None)

        table = Table(table_path, database=self, **kwargs)
        self._tables[name] = table
        return table

    def _ensure_database(self):
        ensure_dir(self._path)

    def _list_table_files(self):
        files = ensure_path_list(os.listdir(self._path))
        return files

    def full_reset(self):
        self._tables = {}
        self._load()

    def _load(self):
        self._ensure_database()
        files = self._list_table_files()
        for f in files:
            self._create_table(f.stem)
    
    def _reload(self):
        self._ensure_database()
        for table in self._tables:
            table._load()
    
    def dump_all(self):
        self._dump()

    def _dump(self):
        self._ensure_database()
        for table in self._tables.values():
            table._dump()

    def __bool__(self):
        return bool(self._tables)

    def __str__(self):
        return str(self._path.resolve())
    
    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return self.get_or_create_table(key)

    def __len__(self):
        return len(self._tables)

    def __iter__(self):
        return iter(self._tables)

    def keys(self):
        return self._tables.keys()

    def values(self):
        return self._tables.values()
        
    def items(self):
        return self._tables.items()