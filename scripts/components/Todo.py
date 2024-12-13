import tkinter as tk
from typing import TypedDict

from scripts.components.Column import StateType
from scripts.components.Entry import Entry, Opts as OptsEntry


class TodoType(TypedDict):
    id: str
    title: str
    state: StateType


class Todo(tk.Frame):
    def __init__(self, master: tk.Frame, data: TodoType, opts: OptsEntry = {}) -> None:
        super().__init__(master)

        self.opts: OptsEntry  = opts
        self.opts["text"] = data["title"]
        Entry(master, self.opts).pack(fill="both", expand=True)
