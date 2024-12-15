import tkinter as tk
from typing import Self, TypedDict

from scripts.components.Column import StateType
from scripts.components.Entry import Entry, Opts as OptsEntry


class TodoType(TypedDict):
    id: str
    title: str
    state: StateType


colors: dict[StateType, str] = {
    "todo": "#d3cfbe",
    "in progress": "#f9d32c",
    "done": "#80b156",
}

class Todo(Entry):
    def __init__(self, master: tk.Frame, data: TodoType, opts: OptsEntry) -> None:
        self.data = data
        self.opts: OptsEntry = opts

        self.opts["state"] = "readonly"
        self.opts["justify"] = "center"
        self.opts["text"] = data["title"]
        self.opts["bg"] = colors[data["state"]]
        self.opts["fg"] = "#000000"

        super().__init__(master, self.opts)

    def create(self) -> Self:
        self.pack(
            fill="x",
            expand=False,
            ipadx=10,
            ipady=10,
        )
        return self

    def set_state(self, state: StateType) -> None:
        self.data["state"] = state

