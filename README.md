# RunDB

RunDb is not exactly a database.
It is similar to [TinyDB](https://tinydb.readthedocs.io/en/stable/) on storing files as json.

The main point of this library is to help the user on storing and loading data.



## Philosophy

* NoSql with tools to simulate relational
* Table are all fully loaded when declared
* Query are done using python
* Data are dict, they all have a unique key as a string



### Quick Overview

```python
import RunDB
from pathlib import Path
from RunDB.tools.serialization import call_kwargs

# Path to DB folder
db_path = Path("testRunDB")
# Create the Database instance
db = RunDB.Database(db_path)

# Get or Create User table, specifying the key as login (default is "id")
# The key is used to find, if not explicitly given, the database id
User = db.table("user", key="login")

# Same for Group table
Group = db.table(
    "group",
    key="name",
    one2many={"users": "user"}
)

# Create User 1
u1 = User.append({"login": "paul"})  # With values

# without values, 
u2 = User["Matthieu"]
u3 = User["Thomas"]

u1.age = 18
u2.age = 20
u3.age = 18

res = User.filter(lambda user: user.age == 20)

list(User.records())


test= Group["test"]
test.users.append(u1)


adminGroup = Group.append({
    "name": "admin",  # as the table key is "name", name will be poped
})


db["test"]["new"] = {"name": "new data"}  # Quick insert

# Check if record has attribute age
"age" in u1  # True

# Get a dict
data = dict(u1.items())

db.dump_all()
```

Nb: Database are simply Group of Table, We can register Tables from somewhere else or simply use a Table without Database object



## Future

* improve relational