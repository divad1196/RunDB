import RunDB
from pathlib import Path
from RunDB.tools.serialization import call_kwargs

db_path = Path("testRunDB")
db = RunDB.Database(db_path)
User = db.table("user", key="login")

u1 = User.append({"login": "paul"})
u2 = User["Matthieu"]
u3 = User["Thomas"]

list(User.records())

Group = db.table("group", key="name", one2many={"users": "user"})

test= Group["test"]
test.users.append(u1)






res = User.filter(lambda d: isinstance(d, dict) and "36" in d["name"])
db["test"]["new"] = {"name": "new data"}

db.table(
    "user",
)
db.table(
    "group",
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
