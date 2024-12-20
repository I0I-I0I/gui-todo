import tkinter as tk

from typing import Any

from scripts.types import ColumnOpts


class Column(tk.Frame):
    def __init__(self, master: tk.Widget, opts: ColumnOpts) -> None:
        master.grid_columnconfigure(opts["index"], weight=1)
        super().__init__(master)

        self.elements: list[tk.Widget] = []

        tk.Label(self, text=opts["title"], font=("Arial", 20)).pack()
        self.grid(row=0, column=opts["index"], sticky="nsew")

    def push(self, el: Any):
        self.elements.append(el)

    def get_elements_count(self) -> int:
        return len(self.elements)

    def remove_all_elements(self) -> None:
        for idx in self.elements:
            idx.destroy()
        for idx in range(self.get_elements_count()):
            self.elements.pop(0)

    def get_element(self, index: int) -> Any:
        return self.elements[index]

    def get_by(self, key, value) -> Any:
        for element in self.elements:
            if element[key] == value:
                return element
        return None

