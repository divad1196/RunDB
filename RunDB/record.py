from . import relational
from .defaults import _sentinelle

_get = object.__getattribute__
_set = object.__setattr__

class Record:
    def __init__(self, table, key, attributes={}, one2many={}):
        _set(self, "_table", table)
        _set(self, "_db", table._db)
        _set(self, "_key", key)
        _set(self, "_attributes", attributes)
        _set(self, "_one2many", one2many)
        # self._table = table
        # self._db = table._db
        # self._key = key
        # self._attributes = attributes
        # self._one2many = one2many

    @property
    def key(self):
        return _get(self, "_key")

    @property
    def table(self):
        return _get(self, "_table")

    @property
    def db(self):
        return _get(self, "_table")._db

    def __str__(self):
        return _get(self, "_key")

    def __repr__(self):
        return str(self)

    def __iter__(self):
        yield self._table._key
        for attr in self._attributes:
            yield attr

    def items(self):
        yield (self._table._key, self.key)
        for attr in self._attributes.items():
            yield attr

    def __getattribute__(self, key):
        keyname = _get(self, "_table")._key
        if key == keyname:
            return _get(self, "_key")

        _attributes = _get(self, "_attributes")
        _one2many = _get(self, "_one2many")

        if key in _one2many:
            value = _attributes.get(key, _sentinelle)
            if value is _sentinelle:
                value = []
                _attributes[key] = value
            table = _get(self, "_table")
            value = relational.One2many(value, _one2many[key], database=table._db)
        elif key in _attributes:
            value = _attributes[key]
        else:
            value = _get(self, key)
        return value
    
    def __setattr__(self, key, value):
        if key == self._table._key:
            raise Exception("Table key can not be changed")
        _get(self, "_attributes")[key] = value
        
    def save(self):
        self._table.save(self)
        