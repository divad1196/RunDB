from .relational import One2many
from .record import Record
from .defaults import _sentinelle
from copy import deepcopy
from .tools.serialization import get_random_id

class RecordSet:
    def __init__(self, table, key="id", one2many={}):
        self._table = table
        self._data = {}
        if not isinstance(key, str):
            raise Exception("key must be of type str")
        self._key = key
        self._one2many = one2many

    def _split_key_data(self, item):
        if not isinstance(item, dict):
            raise Exception("Item must be of type dict")
        copy = deepcopy(item)

        # Handle with default or raise Exception?
        key = copy.pop(self._key, _sentinelle)
        if key is _sentinelle:
            key = get_random_id()
        return key, copy

    def empty_copy(self):
        return RecordSet(
            table=self._table,
            key=self._key,
            one2many=self._one2many
        )

    def append(self, item):
        """
            Add a dict item. Key value must be inside the dict
        """
        key, data = self._split_key_data(item)
        self[key] = data
        return self[key]
    
    def update(self, record):
        """
            Update the value of the record in whole program
        """
        self._data[record.key].update(record._attributes)

    def save(self, record):
        """
            Update the value of the record. No concurrency issue on the record
        """
        self._data[record.key] = record._attributes

    def __bool__(self):
        return bool(self._data)

    def __str__(self):
        return str(list(self._data.keys()))

    def __repr__(self):
        return str(self)

    def get(self, key):
        """
            Same as [] operator but ensure that changing record value won't change value in recordset
        """
        value = self._data.get(key, _sentinelle)
        if value is _sentinelle:
            return Record(self._table, key, {}, one2many=self._one2many)
        return Record(self._table, key, deepcopy(value), one2many=self._one2many)

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise Exception("Indexation is not supported, use record's key")
        value = self._data.get(key, _sentinelle)
        if value is _sentinelle:
            value = {}
            self._data[key] = {}
        return Record(self._table, key, value, one2many=self._one2many)

    def __setitem__(self, key, item):
        if isinstance(item, Record):
            data = item._attributes
            if key != item.key:
                data = deepcopy(data)
        else:
            _, data = self._split_key_data(item)
        self._data[key] = data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self.records()

    def records(self):
        for key, value in self._data.items():
            yield Record(self._table, key, value, one2many=self._one2many)

    def keys(self):
        return self._data.keys()

    def extract(self, keys):
        recordset = self.empty_copy()
        if isinstance(keys, str):
            keys = [keys]
        for k in keys:
            recordset[key] = self[k]._attributes
        return recordset

    def filter(self, condition = None):
        recordset = self.empty_copy()
        if condition is None:
            condition = bool
        for rec in self:
            if condition(rec):
                recordset[rec.key] = rec._attributes
        return recordset

    def __add__(self, recordset):
        if not isinstance(recordset, RecordSet):
            raise Exception("Can only add 2 recordset together")
        res = self.empty_copy()
        res._data = {**self._data, **recordset._data}
        return res

    def __iadd__(self, recordset):
        res = self + recordset
        self._data = res._data
        return self