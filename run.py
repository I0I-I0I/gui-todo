#!/usr/bin/env python
from scripts.app import AppOpts, App
from scripts.db.main import Db


opts: AppOpts = {
    "title": "ToDo Application",
    "width": 720,
    "height": 550,
    "bg": "#000000"
}

db = Db("./db/db.sqlite3")
db.create_db()
db.close()

app = App(opts)
app.mainloop()

