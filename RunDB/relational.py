from . import record
from copy import deepcopy

class One2many:
    def __init__(self, keys, table, database=None):
        self._table = table
        self._db = database
        self._keys = keys
        self._ensure_set()

    def _get_table(self):
        if isinstance(self._table, str):
            self._table = self._db[self._table]
        return self._table

    def _ensure_set(self):
        tmp = set(self._keys)
        if len(tmp) < len(self._keys):
            self._keys.clear()
            self._keys.extend(tmp)

    @property
    def table(self):
        return self._get_table()

    def _get_key(self, index):
        if isinstance(index, str):
            return index
        return self._keys[index]

    def __getitem__(self, index):
        return self.table[self._get_key(index)]
    
    def append(self, key):
        if isinstance(key, record.Record):
            key = key.key
        if key not in self._keys:
            self._keys.append(key)
    
    def __iter__(self):
        for key in self._keys:
            yield self[key]

    def __len__(self):
        return len(self._keys)

    def __str__(self):
        return str(self._keys)

    def __repr__(self):
        return "{table}{keys}".format(
            table=self._get_table()._name,
            keys=self._keys,
        )

    def keys(self):
        return deepcopy(self._keys)



# class Many2many(One2many):
#     def __init__(self, table, relation, database=None, keys=[]):
#         self._relation = relation
#         super(Many2many, self).__init__(table, database, keys)