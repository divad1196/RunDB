

class One2many:
    def __init__(self, table, database=None, keys=[]):
        self._table = table
        self._db = database
        self._keys = keys

    def _get_table(self):
        if isinstance(self._table, str):
            self._table = self._db[self._table]
        return self._table

    def _get_key(self, index):
        if isinstance(index, str):
            return index
        return self._keys[index]

    def __getitem__(self, index):
        return self._get_table()[self._get_key(index)]
    
    def append(self, key):
        self._keys.append(key)
    
    def __iter__(self):
        return iter(self._keys)

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
        return self._keys

    def list(self):
        return [
            self[k]
            for k in self
        ]

    def dict(self):
        return {
            k: self[k]
            for k in self
        }


# class Many2many(One2many):
#     def __init__(self, table, relation, database=None, keys=[]):
#         self._relation = relation
#         super(Many2many, self).__init__(table, database, keys)