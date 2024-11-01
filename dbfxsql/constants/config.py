PATH: str = "~/.config/dbfxsql/config.toml"

TEMPLATE: str = """
[folderpaths]
DBF = ["."]
SQL = ["."]

[extensions]
DBF = [".dbf", ".DBF"]
SQL = [".sql", ".SQL"]

[[relations]]
sources = ["tmp.dbf", "tmp.sql"]
tables = ["", "users"]
fields = [["id", "name"], ["id", "name"]]
"""

VERSION = "0.1.0"
