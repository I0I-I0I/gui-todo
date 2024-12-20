#!/usr/bin/env python
from scripts.app import AppOpts, App


opts: AppOpts = {
    "title": "ToDo Application",
    "width": 720,
    "height": 550,
    "bg": "#000000"
}

app = App(opts)
app.mainloop()

