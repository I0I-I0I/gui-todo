import tkinter as tk

from scripts.components.Entry import Entry, Opts as OptsEntry
from scripts.components.Column import Column, Opts as ColumnOpts, StateType
from scripts.components.Todo import Todo, TodoType


columns: dict[StateType, ColumnOpts] = {
    "todo": {
        "index": 0,
        "uniform": "columns",
        "title": "ToDo"
    },
    "in progress": {
        "index": 1,
        "uniform": "columns",
        "title": "In Progress"
    },
    "done": {
        "index": 2,
        "uniform": "columns",
        "title": "Done"
    }
}

todo_list: list[TodoType] = [
    {
        "id": "1",
        "title": "Learn Python",
        "state": "done",
    },
    {
        "id": "2",
        "title": "Learn JavaScrip",
        "state": "in progress",
    },
    {
        "id": "3",
        "title": "Learn React",
        "state": "in progress",
    },
    {
        "id": "4",
        "title": "Learn Angular",
        "state": "todo",
    },
]

class HomePage(tk.Frame):
    def __init__(self, master: tk.Frame, opts = {}) -> None:
        super().__init__(master)

        self.config(opts)
        self.columns: dict[StateType, Column] = self._create_columns(columns)
        self.todo_opts = OptsEntry(
            placeholder = "Add a task",
            bg = "#ffffff",
            fg = "#000000",
            state = "normal",
        )

        self.create_todo_list(self.todo_opts)

    def create_todo_list(self, todo_opts: OptsEntry) -> None:
        for todo_data in todo_list:
            current_column = self.columns[todo_data["state"]]
            todo: Todo = Todo(current_column, todo_data, todo_opts).create()
            current_column.push(todo)

        todo_col = self.columns["todo"]
        opts = OptsEntry(
            justify = "center",
            bg = "#d9d9d9",
            placeholder = "Add todo"
        )
        Entry(todo_col, opts).pack(
            fill="x",
            expand=False,
            ipadx=10,
            ipady=10,
        )

    def _create_columns(self, columns_list: dict[StateType, ColumnOpts]) -> dict[StateType, Column]:
        columns: dict[StateType, Column] = {}
        for column in columns_list:
            columns[column] = Column(self, columns_list[column])
        return columns

