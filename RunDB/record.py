from .relational import One2many

_get = object.__getattribute__

class Record:
    def __init__(self, table, key, attributes={}, one2many={}):
        self._table = table
        self._key = key
        self._attributes = attributes
        self._one2many = one2many

    @property
    def key(self):
        return _get(self, "_key")

    @property
    def table(self):
        return _get(self, "_table")

    @property
    def db(self):
        return _get(self, "_table")._db


    def __getattribute__(self, key):
        _attributes = _get(self, _attributes)
        if key in _attributes:
            value = _attributes[value]
            _one2many = _get(self, "_one2many")
            if key in _one2many:
                table = _get(self, "_table")
                One2many(table, database=table._db, keys=value):
        else:
            value = _get(self, key)
        
    def save(self):
        self._table.save(self)
        