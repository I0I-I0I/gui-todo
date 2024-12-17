from dataclasses import asdict, dataclass, field
from typing import Any, Callable, List, Literal, Self, TypedDict

import tkinter as tk


@dataclass
class CustomInnerOpts:
    cb: Callable[[Any], None]
    value: str

class CustomOpts(TypedDict):
    placeholder: CustomInnerOpts
    state: CustomInnerOpts

StateType = Literal["normal", "disabled", "readonly"]

custom = ["placeholder", "placeholder_fg", "state", "_custom"]

@dataclass
class Opts:
    bg: str = "#000000"
    fg: str = "#ffffff"
    text: str = ""
    width: int = 20
    font: tuple[str, int] = ("Arial", 12)
    state: StateType = "normal"
    justify: str = ""
    cursor: str = ""
    readonlybackground: str = "grey"

    placeholder: str = ""
    placeholder_fg: str = "grey"

    _custom: List[str] = field(default_factory=lambda: custom)

    def __getitem__(self, key) -> object:
        return getattr(self, key)

    def get_dict(self) -> dict[str, Any]:
        return asdict(self)

class Entry(tk.Entry):
    def __init__(self, master: tk.Frame, opts_: Opts) -> None:
        super().__init__(master)

        self.opts: Opts = opts_
        self.custom_opts = self._get_custom_opts(opts_)

        self.setup()

    def _setup_custom_opts(self) -> None:
        for key in self.opts.get_dict():
            if key in self.opts._custom:
                if self.custom_opts.get(key):
                    self.custom_opts[key].cb(self.opts[key])
                continue

    def setup(self) -> None:
        self._setup_custom_opts()
        cnf = {}
        for key in self.opts.get_dict():
            if key in ["placeholder", "placeholder_fg", "_custom"]: continue
            cnf[key] = self.opts[key]

        if self.opts.text:
            self.set_text(self.opts.text)
        else:
            cnf["fg"] = self.opts.placeholder_fg

        self.config(cnf)

    def set_placeholder(self, placeholder: str):
        self.opts.placeholder = placeholder
        self.custom_opts["placeholder"].value = self.opts.placeholder
        self.set_text(placeholder)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def set_text(self, text) -> None:
        self.delete(0, tk.END)
        self.insert(0, text)

    def _set_state(self, state: StateType) -> None:
        self.custom_opts["state"].value = self.opts.state
        self.opts.state = state
        if state == "readonly":
            self.opts.cursor = "arrow"
            self.opts.readonlybackground = self.opts.bg
        elif state == "disabled":
            self.opts.fg = "grey"
            self.opts.cursor = "arrow"

    def _on_focus_in(self, _) -> None:
        if self.get() == self.custom_opts["placeholder"].value:
            self.delete(0, tk.END)
            self.config(fg = self.opts.fg)

    def _on_focus_out(self, _) -> None:
        if self.get() == "":
            self.insert(0, self.custom_opts["placeholder"].value)
            self.config(fg = self.opts.placeholder_fg)

    def _get_custom_opts(self, opts: Opts) -> CustomOpts:
        custom_opts: CustomOpts = {
            "placeholder": CustomInnerOpts(
                cb = self.set_placeholder,
                value = ""
            ),
            "state": CustomInnerOpts(
                cb = self._set_state,
                value = opts.state
            ),
        }
        return custom_opts

    def create(self, opts = None) -> Self:
        opts = opts or {
            "fill": "x",
            "expand": False,
            "ipadx": 10,
            "ipady": 10,
        }
        self.pack(opts)
        return self

