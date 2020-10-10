import RunDB
from pathlib import Path
from RunDB.tools.serialization import call_kwargs

db_path = Path("testRunDB")
db = RunDB.Database(db_path)
User = db.table("user", key="login")

Group = db.table(
    "group",
    key="name",
    one2many={"users": "user"}
)


u1 = User.append({"login": "paul"})
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

db.dump_all()