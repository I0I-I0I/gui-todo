import tkinter as tk

from typing import Any, Literal, NotRequired, TypedDict


StateType = Literal["done", "in progress", "todo"]

class Opts(TypedDict):
    index: int
    uniform: str
    title: str
    weight: NotRequired[int]
    bg: NotRequired[str]
    fg: NotRequired[str]


class Column(tk.Frame):
    def __init__(self, master: tk.Frame, opts: Opts) -> None:
        master.grid_columnconfigure(opts["index"], weight=1)
        super().__init__(master)

        self.elements: list[Any] = []

        tk.Label(self, text=opts["title"], font=("Arial", 20)).pack()
        self.grid(row=0, column=opts["index"], sticky="nsew")

    def push(self, el: Any):
        self.elements.append(el)

    def get_element(self, index: int) -> Any:
        return self.elements[index]

    def get_by(self, key, value) -> Any:
        for element in self.elements:
            if element[key] == value:
                return element
        return None

