# RunDB

RunDb is not exactly a database.
It is similar to [TinyDB](https://tinydb.readthedocs.io/en/stable/) on storing files as json.

The main point of this library is to help the user on storing and loading data.



## Philosophy

* NoSql with tools to simulate relational
* Table are all fully loaded when declared
* Query are done using python
* Data must be serializable, but no format is imposed: some data may be stored as dict, while other are mere strings
  some utilities functions may expect specific values, but it is recommended to only store Dict[str, Any] with string as key
* No Opinion, let user defines hooks



```python
import RunDB
from pathlib import Path

db_path = Path("testRunDB")  # The folder containing the tables as json files

db = RunDB.Database(db_path)  # This will create the folder if it is missing, then loading all tables
User = db.table("user")  # Create or get table labeled as "user", it's file is called user.json
User["hello"] = {"name": "World"}

res = User.filter(lambda d: isinstance(d, dict) and "36" in d["name"])  # return a subtable as a dict

new = {"name": "new data"}
db["test"]["new"] = new
new.update({"option": "some text"}) # This will also update the value in the database

db.dump_all()  # Dump all tables

```



Nb: Database are simply Group of Table, We can register Tables from somewhere else or simply use a Table without Database object

## Wrapping

You may want to use custom object.

```python
from RunDB.tools.serialization import call_kwargs

db = RunDB.Database(...)

class User:
    def __init__(self, name, password, admin=False, groups=[]):
        self.name = name
        self.pwd = password
        self.admin = admin
        self.groups = db.One2many("group", groups)

def dict_to_user(obj):
    return call_kwargs(User, obj)

def user_to_dict(obj):
    return {
        "name": obj.name,
        "password": obj.pwd,
        "admin": obj.admin,
    }

class Group:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return "Group {name}".format(name=self.name)

def dict_to_group(obj):
    return call_kwargs(Group, obj)

def group_to_dict(obj):
    return {
        "name": obj.name,
        "value": obj.value,
    }

def group_default_key(obj):
    return obj.name

db.table(
    "user",
    # Both parameter below should use validator if needed, as pydantic, marshmallow, schema, cerberus, ...
    serializer=user_to_dict,  # How to save an object
    deserializer=dict_to_user,  # How return an object 
)
db.table(
    "group",
    serializer=group_to_dict,
    deserializer=dict_to_group,
    anonymous=group_default_key,  # how to retrieve the object key with Table.append method
)

u = User("paul", "passWord", groups=["first", "other"])
g1 = Group("first", 5)
g2 = Group("second", 9)
g3 = Group("other", 7)

db["user"][u.name] = u
db["group"].append(g1)
db["group"].append(g2)
db["group"].append(g3)

u.groups.list()

db.dump_all()
```





## Future

* Abstract dump and loading
* Define other dumps
* improve relational
* improve object mapping