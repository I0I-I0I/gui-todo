import tkinter as tk
from scripts.pages.HomePage import HomePage

from typing import NotRequired, TypedDict


class Opts(TypedDict):
    title: str
    width: int
    height: int
    bg: str
    icon: NotRequired[str]


class App(tk.Tk):
    def __init__(self, opts: Opts) -> None:
        super().__init__()

        self.title(opts["title"])
        self.geometry(f"{opts["width"]}x{opts["height"]}")
        self.resizable(True, True)
        if "icon" in opts:
            self.iconphoto(False, tk.PhotoImage(file=opts["icon"]))

        container = tk.Frame(self, bg=opts["bg"])
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.HomePage = HomePage

        frame = HomePage(container)
        self.frames[HomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, container: type) -> None:
        # menubar = frame.create_menubar(self)
        # self.configure(menu=menubar)
        frame = self.frames[container]
        frame.tkraise()

