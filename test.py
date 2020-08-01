import RunDB
from pathlib import Path
db_path = Path("testRunDB")
db = RunDB.Database(db_path)
User = db.table("user")

res = User.filter(lambda d: isinstance(d, dict) and "36" in d["name"])
db["test"]["new"] = {"name": "new data"}
alpha = RunDB.One2many("abcde", db)
alpha.append("a")
alpha.append("b")
alpha.append("h")
alpha.append("j")

