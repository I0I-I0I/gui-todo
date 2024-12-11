from typing import Any, Dict, NotRequired, TypedDict

import tkinter as tk


class Opts(TypedDict):
    bg: str
    fg: str
    placeholder: NotRequired[str]
    width: NotRequired[int]
    height: NotRequired[int]


class SetupOpts(TypedDict):
    width: NotRequired[int]
    height: NotRequired[int]
    pady: NotRequired[int]
    padx: NotRequired[int]


class Entry(tk.Entry):
    def __init__(self, master: tk.Frame, opts: Opts = {
        "bg": "#ffffff",
        "fg": "#000000"
    }) -> None:
        super().__init__(master)

        self.master = master
        self.opts = opts
        self.default_setup_opts: SetupOpts = {
            "pady": 0,
            "padx": 0
        }

        config_opts: Dict[str, Any] = {
            "bg": self.opts["bg"],
            "fg": self.opts["fg"]
        }
        self.config(config_opts)

    def setup(self, setup_opts: SetupOpts) -> None:
        if "placeholder" in self.opts:
            self.insert(0, self.opts["placeholder"])
            self.bind("<FocusIn>", self._on_focus_in)
            self.bind("<FocusOut>", self._on_focus_out)
            self.config(fg = "grey")

        self.default_setup_opts.update(setup_opts)

        self.pack(
            pady=self.default_setup_opts["pady"],
            padx=self.default_setup_opts["padx"],
        )

    def _on_focus_in(self, _):
        if not "placeholder" in self.opts: return
        if self.get() == self.opts["placeholder"]:
            self.delete(0, tk.END)
            self.config(fg='black')

    def _on_focus_out(self, _):
        if not "placeholder" in self.opts: return
        if self.get() == "":
            self.insert(0, self.opts["placeholder"])
            self.config(fg='grey')

