from typing import  Self

import tkinter as tk

from scripts.types import EntryCustomInnerOpts, EntryCustomOpts, EntryMainOptsList, EntryOpts, EntryStateType


class Entry(tk.Entry):
    def __init__(self, master: tk.Frame, opts: EntryOpts) -> None:
        super().__init__(master)

        self.opts_entry: EntryMainOptsList = {
            "bg": "#ffffff",
            "fg": "#000000",
            "text": "",
            "width": 20,
            "font": ("Arial", 12),
            "state": "normal",
            "justify": "",
            "cursor": "",
        }
        self.opts_entry.update(opts.opts)

        cust_opts = self._get_custom_opts(opts._custom)
        self.custom: EntryCustomOpts = cust_opts if cust_opts else {}
        self.setup()

    def _setup_custom_opts(self) -> None:
        for key in self.custom:
            opt = self.custom[key]
            opts = self.opts_entry.get(key)
            if type(opt) is str or opts is None: continue
            opt.cb(self.opts_entry[key])

    def setup(self) -> None:
        self._setup_custom_opts()
        cnf = {}
        for key in self.opts_entry:
            if key not in EntryCustomOpts.__annotations__.keys():
                cnf[key] = self.opts_entry[key]

        if self.opts_entry.get("text"):
            self.set_text(self.opts_entry.get("text"))
        else:
            plch = self.opts_entry.get("placeholder")
            pl = self.custom.get("placeholder")
            if plch and pl:
                pl.cb(plch)
            plch_fg = self.custom.get("placeholder_fg")
            cnf["fg"] = plch_fg if plch_fg else self.opts_entry.get("fg")

        self.config(cnf)

    def set_placeholder(self, placeholder: str):
        plch = self.custom.get("placeholder")
        if plch is None: return
        plch.value = placeholder
        self.set_text(placeholder)
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def set_text(self, text) -> None:
        self.delete(0, tk.END)
        self.insert(0, text)

    def _set_state(self, state: EntryStateType) -> None:
        ost = self.opts_entry.get("state")
        cst = self.custom.get("state")
        if ost is None or cst is None: return
        cst.value = ost
        self.opts_entry["state"] = state
        if state == "readonly":
            self.opts_entry["cursor"] = "arrow"
            # bg = self.opts_entry.get("bg")
            # if bg is None: return
            # self.opts_entry["readonlybackground"] = bg
        elif state == "disabled":
            self.opts_entry["fg"] = "grey"
            self.opts_entry["cursor"] = "arrow"

    def _on_focus_in(self, _) -> None:
        plch = self.custom.get("placeholder")
        if plch is None: return
        if self.get() == plch.value:
            self.delete(0, tk.END)
            fg = self.opts_entry.get("fg")
            if fg is None: return
            self.config(fg=fg)

    def _on_focus_out(self, _) -> None:
        plch = self.custom.get("placeholder")
        plch_fg = self.custom.get("placeholder_fg")
        if plch is None or plch_fg is None: return
        if self.get() == "":
            self.insert(0, plch.value)
            self.config(fg = plch_fg)

    def _get_custom_opts(self, opts: EntryCustomOpts) -> EntryCustomOpts | None:
        st = opts.get("state")
        st = st if st else "normal"
        custom_opts = EntryCustomOpts(
            placeholder = EntryCustomInnerOpts(
                cb = self.set_placeholder,
                value = ""
            ),
            state = EntryCustomInnerOpts(
                cb = self._set_state,
                value = "normal"
            ),
            placeholder_fg="grey"
        )
        return custom_opts

    def create(self, **opts) -> Self:
        opts = opts or {
            "fill": "x",
            "expand": False,
            "ipadx": 10,
            "ipady": 10,
        }
        self.pack(**opts)
        return self

