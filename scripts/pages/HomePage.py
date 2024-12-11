import tkinter as tk

from scripts.components.Entry import Entry


class HomePage(tk.Frame):
    def __init__(self, parent, container) -> None:
        super().__init__(container)

        label = tk.Label(self, text="Home Page")
        label.pack(pady=0, padx=0)

        Entry(self, opts={
            "placeholder": "Project Name",
            "bg": "#ffffff",
            "fg": "#000000"
        }).setup({
            "pady": 10
        })

        Entry(self, opts={
            "placeholder": "ToDo Name",
            "bg": "#ffffff",
            "fg": "#000000"
        }).setup({
            "pady": 10
        })

        button = tk.Button(self, text="Next", command=lambda: parent.show_frame(parent.Validation))
        button.pack(pady=10)

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

