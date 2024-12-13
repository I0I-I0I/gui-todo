import tkinter as tk

from scripts.components.Entry import Opts as OptsEntry
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
    def __init__(self, master: tk.Frame) -> None:
        super().__init__(master)

        self.columns: dict[StateType, Column] = self._create_columns(columns)
        todo_opts: OptsEntry = {
            "placeholder": "Add a task",
            "bg": "#ffffff",
            "fg": "#000000",
            "state": "normal",
        }

        for todo_data in todo_list:
            current_column = self.columns[todo_data["state"]]
            todo: Todo = Todo(current_column, todo_data, todo_opts)
            current_column.push(todo)

    def create_menubar(self, parent):
        menubar = tk.Menu(parent, bd=3, relief=tk.RAISED, activebackground="#80B9DC")

        filemenu = tk.Menu(menubar, tearoff=0, relief=tk.RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Project", command=lambda: parent.show_frame(parent.Validation))
        filemenu.add_command(label="Close", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)

        processing_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Validation", menu=processing_menu)
        processing_menu.add_command(label="validate")
        processing_menu.add_separator()

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_separator()

        return menubar

    def _create_columns(self, columns_list: dict[StateType, ColumnOpts]) -> dict[StateType, Column]:
        columns: dict[StateType, Column] = {}
        for column in columns_list:
            columns[column] = Column(self, columns_list[column])
        return columns

