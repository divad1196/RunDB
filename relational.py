

class One2many:
    def __init__(self, table, database=None):
        self._table = table
        self._db = database
        self._keys = []

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

    def all(self):
        data = {}
        for k in self:
            data[k] = self[k]
        return data