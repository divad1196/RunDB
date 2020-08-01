# RunDB

RunDb is not exactly a database.
It is similar to [TinyDB](https://tinydb.readthedocs.io/en/stable/) on storing files as json.

The main point of this library is to help the user on storing and loading data.



## Philosophy

* NoSql with tools to simulate relational
* Table are fully loaded
* Query are done using python
* Data must be serializable, but no format is imposed: some data may be stored as dict, while other are mere strings
* You can specify a serialization and deserialization function to automaticly convert the values



```python
import RunDB
from pathlib import Path

db_path = Path("testRunDB")  # The folder containing the tables as json files

db = RunDB.Database(db_path)  # This will create the folder if it is missing, then loading all tables
User = db.table("user")  # Create or get table labeled as "user", it's file is called user.json
User["hello"] = {"name": "World"}

res = User.filter(lambda d: isinstance(d, dict) and "36" in d["name"])  // return a subtable

db["test"]["new"] = {"name": "new data"}

db.dump_all()  # Dump all tables

```



Nb: Database are simply Group of Table, We can register Tables from somewhere else or simply use a Table without Database object



## Future

* add other serialization as csv or yaml
* 