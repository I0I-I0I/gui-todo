import tkinter as tk

from scripts.components.Column import Column
from scripts.components.Entry import Entry
from scripts.db.main import Db
from scripts.types import TodoDataType, TodoStateType


colors: dict[TodoStateType, str] = {
    TodoStateType.TODO: "#d3cfbe",
    TodoStateType.IN_PROGRESS: "#f9d32c",
    TodoStateType.DONE: "#80b156",
}

class Todo(tk.Frame):
    def __init__(self, master: Column, data: TodoDataType, opts) -> None:
        super().__init__(master)

        self._master = master
        self.data = data
        self.entry_opts = opts["entry"].opts
        self.cbs = opts["entry"].cbs
        self.opts = opts

        self.state: TodoStateType = data["state"]
        self.opts["entry"].opts["state"] = "readonly"
        self.opts["entry"].opts["justify"] = "center"
        self.opts["entry"].opts["text"] = data["title"]
        self.opts["entry"].opts["bg"] = colors[self.state]

    def create(self):
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.X)

        self.entry = Entry(self.frame, self.opts["entry"])
        self.button_edit = tk.Button(self.frame, text="Edit", command=self.open_popup)
        self.button_delete = tk.Button(self.frame, text="X", command=self._on_delete)

        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.button_edit.pack(side=tk.LEFT)
        self.button_delete.pack(side=tk.LEFT)

        self.pack(side=tk.TOP, fill=tk.X)

        self.set_binds()
        return self

    def destroy(self) -> None:
        super().destroy()
        self.frame.destroy()
        self.entry.destroy()
        self.button_edit.destroy()
        self.button_delete.destroy()

    def set_binds(self) -> None:
        self.entry.bind("<Button-1>", self._on_click)
        self.entry.bind("<Button-3>", self._on_right_click)

    def _on_delete(self) -> None:
        id = self.data.get("id")
        if id is None: return
        db = Db("./db/db.sqlite3")
        db.delete("todos", id)
        db.close()
        self.cbs["on_click_todo"]("")

    def open_popup(self):
        self.popup = tk.Toplevel(self._master)
        self.popup.title("Add New To-Do")

        self.popup_label = tk.Label(self.popup, text="Enter new to-do item:")
        self.popup_label.pack(pady=5)

        self.popup_entry = tk.Entry(self.popup, width=30)
        self.popup_entry.pack(pady=5)
        self.popup_entry.insert(0, self.entry.get())

        self.save_button = tk.Button(self.popup, text="Save", command=self.save_todo)
        self.save_button.pack(pady=5)

    def save_todo(self) -> None:
        id = self.data.get("id")
        value = self.popup_entry.get()
        if id is None: return
        if value == "": return
        db = Db("./db/db.sqlite3")
        db.update("todos", id, {
            "title": value
        })
        db.close()
        self.popup.destroy()
        self.cbs["on_click_todo"]("")

    def _on_click(self, _) -> None:
        id = self.data.get("id")
        if id is None: return
        self.state = self.state.update_state()
        db = Db("./db/db.sqlite3")
        db.update("todos", id, { "state": self.state.name })
        db.close()
        self.cbs["on_click_todo"](_)

    def _on_right_click(self, _) -> None:
        id = self.data.get("id")
        if id is None: return
        self.state = self.state.update_state(-1)
        db = Db("./db/db.sqlite3")
        db.update("todos", id, { "state": self.state.name })
        db.close()
        self.cbs["on_click_todo"](_)

    def set_state(self, state: TodoStateType) -> None:
        self.data["state"] = state

