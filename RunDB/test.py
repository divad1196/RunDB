import RunDB
from pathlib import Path
from RunDB.tools.serialization import call_kwargs

db_path = Path("testRunDB")
db = RunDB.Database(db_path)
User = db.table("user")

res = User.filter(lambda d: isinstance(d, dict) and "36" in d["name"])
db["test"]["new"] = {"name": "new data"}

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
    serializer=user_to_dict,
    deserializer=dict_to_user,
)
db.table(
    "group",
    serializer=group_to_dict,
    deserializer=dict_to_group,
    anonymous=group_default_key,
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
