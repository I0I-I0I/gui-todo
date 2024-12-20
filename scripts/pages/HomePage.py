import tkinter as tk

from scripts.components.Entry import Entry
from scripts.components.Column import Column
from scripts.components.Todo import Todo
from scripts.db.main import Db

from scripts.types import ColumnOpts, EntryMainOptsList, EntryOpts, TodoDataType, TodoStateType


columns: dict[TodoStateType, ColumnOpts] = {
    TodoStateType.TODO: {
        "index": 0,
        "uniform": "columns",
        "title": "ToDo"
    },
    TodoStateType.IN_PROGRESS: {
        "index": 1,
        "uniform": "columns",
        "title": "In Progress"
    },
    TodoStateType.DONE: {
        "index": 2,
        "uniform": "columns",
        "title": "Done"
    }
}

class HomePage(tk.Frame):
    def __init__(self, master: tk.Frame, opts = {}) -> None:
        super().__init__(master)

        self.config(opts)
        self.columns: dict[TodoStateType, Column] = self._create_columns(columns)
        self.todo_opts = {}
        self.todo_opts["entry"] = EntryOpts(
            opts={
                "bg": "#ffffff",
                "fg": "#000000",
                "state": "normal",
            },
            cbs={
                "on_click_todo": self._on_click_todo
            }
        )
        self.todo = {
            "placeholder": "",
        }

        self._create_todo_list()

    def _create_add_entry(self) -> None:
        todo_col = self.columns[TodoStateType.TODO]
        self.todo["placeholder"] = "Add a task"
        opts = EntryOpts(
            opts=EntryMainOptsList(
                justify = "center",
                bg = "#d9d9d9",
                state = "normal",
                placeholder = self.todo["placeholder"]
            ),
        )
        plch = opts._custom.get("placeholder")
        if plch:
            plch.value = self.todo["placeholder"]

        self.add_entry = Entry(todo_col, opts)
        self.add_entry.pack(
            fill="x",
            expand=False,
            ipadx=10,
            ipady=10,
        )
        self.add_entry.bind("<Return>", self._on_entry_focus_out)

    def _create_todo_list(self) -> None:
        for column in self.columns:
            current_column = self.columns[column]
            current_column.remove_all_elements()

        try:
            self.add_entry.destroy()
        except AttributeError:
            pass

        db = Db("./db/db.sqlite3")
        data = db.get_all("todos")
        todo_list: list[TodoDataType] = []
        for item in data:
            todo_list.append({
                "id": item[0],
                "ordering": item[1],
                "state": TodoStateType.set_type(item[2]),
                "title": item[3],
                "date": item[4],
            })
        db.close()
        for todo_data in todo_list:
            current_column = self.columns[todo_data["state"]]
            todo: Todo = Todo(current_column, todo_data, self.todo_opts).create()
            current_column.push(todo)

        self._create_add_entry()

    def _on_entry_focus_out(self, event: tk.Event) -> None:
        value = event.widget.get()
        if not value or value == self.todo["placeholder"]:
            return
        state = TodoStateType.TODO
        event.widget.unbind("<Return>")
        event.widget.destroy()

        todo_data: TodoDataType = {
            "id": "3",
            "title": value,
            "state": state,
            "ordering": 2
        }
        current_column = self.columns[state]
        todo: Todo = Todo(current_column, todo_data, self.todo_opts).create()
        current_column.push(todo)

        db = Db("./db/db.sqlite3")
        db.insert("todos", {
            "ordering": 3,
            "title": todo_data["title"],
            "state": todo_data["state"].name,
        })
        db.close()

        self._create_add_entry()

    def _create_columns(self, columns_list: dict[TodoStateType, ColumnOpts]) -> dict[TodoStateType, Column]:
        columns: dict[TodoStateType, Column] = {}
        for column in columns_list:
            columns[column] = Column(self, columns_list[column])
        return columns

    def _on_click_todo(self, event) -> None:
        self._create_todo_list()


