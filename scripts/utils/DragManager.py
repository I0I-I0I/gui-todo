from typing import Any, Callable, TypedDict
import tkinter as tk


class CursorCoordsType(TypedDict):
    x: int
    y: int

class PointType(TypedDict):
    x: tuple[int, int]
    y: tuple[int, int]

AriasType = dict[str, PointType]


class DragManager():
    def __init__(self, target, arias: AriasType) -> None:
        self.target = target
        self.arias = arias

    def add_draggable(self, cb: Callable[[Any, CursorCoordsType], None]):
        self.cb = cb

        self.target.bind("<ButtonPress-1>", self._on_start)
        self.target.bind("<B1-Motion>", self._on_drag)
        self.target.bind("<ButtonRelease-1>", self._on_drop)
        self.target.configure(cursor="hand1")

    def _on_start(self, event: tk.Event):
        pass

    def _on_drag(self, event: tk.Event):
        pass

    def _on_drop(self, event: tk.Event) -> str | None:
        coords: CursorCoordsType = {
            "x": event.x,
            "y": event.y
        }
        self.cb(self.target, coords)

        for key in self.arias:
            aria = self.arias[key]
            cursor_x = coords["x"]
            cursor_y = coords["x"]
            x_from = aria["x"][0]
            x_to = aria["x"][1]
            y_from = aria["y"][0]
            y_to = aria["y"][1]
            if (cursor_x >= x_from and cursor_x <= x_to) and (cursor_y >= y_from and cursor_y <= y_to):
                return key
        return None

