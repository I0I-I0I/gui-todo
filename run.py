#!/usr/bin/env python
from scripts.app import Opts, App


opts: Opts = {
    "title": "ToDo Application",
    "width": 720,
    "height": 550,
    "bg": "#000000"
}

app = App(opts)
app.mainloop()

