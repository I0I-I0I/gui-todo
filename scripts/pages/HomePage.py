import tkinter as tk

from typing import Any

from scripts.components.Entry import Opts as OptsEntry
from scripts.components.Column import Column, Opts as ColumnOpts, StateType
from scripts.components.Todo import Todo, TodoType
from scripts.utils.DragManager import AriasType, CursorCoordsType, DragManager, PointType


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

def get_coords(target: Any) -> PointType:
    x_from = target.winfo_x()
    x_to = x_from + target.winfo_width()
    y_from = target.winfo_y()
    y_to = y_from + 600
    return {
        "x": (x_from, x_to),
        "y": (y_from, y_to)
    }


class HomePage(tk.Frame):
    def __init__(self, master: tk.Frame) -> None:
        super().__init__(master)

        self.window_size: dict[str, int] = {
            "width": master.winfo_screenwidth(),
            "height": master.winfo_screenheight()
        }
        self.columns: dict[StateType, Column] = self._create_columns(columns)
        self.todo_opts: OptsEntry = {
            "placeholder": "Add a task",
            "bg": "#ffffff",
            "fg": "#000000",
            "state": "normal",
        }
        self.arias: AriasType = {}

        def s(event):
            for column in self.columns:
                self.arias[column] = get_coords(self.columns[column])

        def on_drop(target, coords: CursorCoordsType) -> None:
            print(target)
            print(self.arias)

        for column in self.columns:
            dnd = DragManager(self.columns[column], self.arias)
            dnd.add_draggable(on_drop)

        self.create_todo_list(self.todo_opts)
        self.columns["todo"].bind("<Visibility>", s)

    def create_todo_list(self, todo_opts: OptsEntry) -> None:
        for todo_data in todo_list:
            current_column = self.columns[todo_data["state"]]
            todo: Todo = Todo(current_column, todo_data, todo_opts).create()
            current_column.push(todo)

    def _create_columns(self, columns_list: dict[StateType, ColumnOpts]) -> dict[StateType, Column]:
        columns: dict[StateType, Column] = {}
        for column in columns_list:
            columns[column] = Column(self, columns_list[column])
        return columns

