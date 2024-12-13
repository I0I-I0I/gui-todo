from typing import Any, Literal, Mapping, NotRequired, TypedDict

import tkinter as tk


StateType = Literal["normal", "disabled", "readonly"]
class Opts(TypedDict):
    bg: NotRequired[str]
    fg: NotRequired[str]
    text: NotRequired[str]
    placeholder: NotRequired[str]
    width: NotRequired[int]
    font: NotRequired[tuple[str, int]]
    state: NotRequired[StateType]


class Entry(tk.Entry):
    def __init__(self, master: tk.Frame, opts: Opts = {
        "bg": "#ffffff",
        "fg": "#000000"
    }) -> None:
        super().__init__(master)

        self.opts = {}
        self.custom_opts = self._get_custom_opts()

        custom_opts_list: list[str] = []

        for key in opts:
            if key in self.custom_opts:
                custom_opts_list.append(key)
                continue
            self.opts[key] = opts[key]
        self.config(self.opts)

        for key in custom_opts_list:
            if key in self.custom_opts:
                self.custom_opts[key]["cb"](opts[key])

        if "text" in opts:
            self.set_text(opts["text"])

    def set_placeholder(self, placeholder: str):
        self.set_text(placeholder)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self.config(fg = "grey")
        self.custom_opts["placeholder"]["value"] = placeholder

    def set_text(self, text) -> None:
        self.delete(0, tk.END)
        self.insert(0, text)

    def _set_state(self, state: StateType) -> None:
        self.config(state=state)
        if state == "readonly":
            self.config(cursor="arrow")
        elif state == "normal":
            self.config(fg="black")
        elif state == "disabled":
            self.config(fg="grey", bg="grey")
            self.config(cursor="arrow")

    def _on_focus_in(self, _) -> None:
        if self.get() == self.custom_opts["placeholder"]["value"]:
            self.delete(0, tk.END)
            self.config(fg='black')

    def _on_focus_out(self, _) -> None:
        if self.get() == "":
            self.insert(0, self.custom_opts["placeholder"]["value"])
            self.config(fg='grey')

    def _get_custom_opts(self) -> Mapping[str, Any]:
        return {
            "placeholder": {
                "cb": self.set_placeholder,
                "value": ""
            },
            "state": {
                "cb": self._set_state
            }
        }

