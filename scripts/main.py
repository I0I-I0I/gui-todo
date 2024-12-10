import tkinter as tk


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Sample Tkinter Structuring")
        self.geometry("720x550")
        self.resizable(True, True)
        # self.iconphoto(False, tk.PhotoImage(file="assets/title_icon.png"))

        container = tk.Frame(self, bg="#191919")
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.HomePage = HomePage

        frame = HomePage(self, container)
        self.frames[HomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, container) -> None:
        frame = self.frames[container]
        menubar = frame.create_menubar(self)
        self.configure(menu=menubar)
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, container) -> None:
        super().__init__(container)

        label = tk.Label(self, text="Home Page")
        label.pack(pady=0, padx=0)

    def create_menubar(self, parent):
        menubar = tk.Menu(parent, bd=3, relief=tk.RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = tk.Menu(menubar, tearoff=0, relief=tk.RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New Project", command=lambda: parent.show_frame(parent.Validation))
        filemenu.add_command(label="Close", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.quit)

        ## proccessing menu
        processing_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Validation", menu=processing_menu)
        processing_menu.add_command(label="validate")
        processing_menu.add_separator()

        ## help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_separator()

        return menubar


if __name__ == "__main__":
    app = App()
    app.mainloop()

