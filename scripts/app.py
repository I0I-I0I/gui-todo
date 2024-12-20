import tkinter as tk
from scripts.pages.HomePage import HomePage

from scripts.types import AppOpts


class App(tk.Tk):
    def __init__(self, opts: AppOpts) -> None:
        super().__init__()

        self.title(opts["title"])
        self.resizable(True, True)

        if "icon" in opts:
            self.iconphoto(False, tk.PhotoImage(file=opts["icon"]))

        container = tk.Frame(self, bg=opts["bg"])
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.HomePage = HomePage

        frame = HomePage(container, {
            "bg": opts["bg"]
        })
        self.frames[HomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, container: type) -> None:
        # menubar = frame.create_menubar(self)
        # self.configure(menu=menubar)
        frame = self.frames[container]
        frame.tkraise()

