from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Literal, NotRequired, TypedDict


class AppOpts(TypedDict):
    title: str
    width: int
    height: int
    bg: str
    icon: NotRequired[str]

class ColumnOpts(TypedDict):
    index: int
    uniform: str
    title: str
    weight: NotRequired[int]
    bg: NotRequired[str]
    fg: NotRequired[str]

class TodoStateType(Enum):
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2

    @staticmethod
    def set_type(type):
        self: TodoStateType
        match type:
            case "TODO":
                self = TodoStateType.TODO
            case "IN_PROGRESS":
                self = TodoStateType.IN_PROGRESS
            case "DONE":
                self = TodoStateType.DONE
            case _:
                raise ValueError("Invalid TodoStateType")
        return self

    def update_state(self, idx: int = 1):
        match self:
            case TodoStateType.TODO:
                if idx == -1:
                    return TodoStateType.DONE
                return TodoStateType.IN_PROGRESS
            case TodoStateType.IN_PROGRESS:
                if idx == -1:
                    return TodoStateType.TODO
                return TodoStateType.DONE
            case TodoStateType.DONE:
                if idx == -1:
                    return TodoStateType.IN_PROGRESS
                return TodoStateType.TODO

    def get_name(self) -> str:
        match self:
            case TodoStateType.TODO:
                return "TODO"
            case TodoStateType.IN_PROGRESS:
                return "IN_PROGRESS"
            case TodoStateType.DONE:
                return "DONE"


EntryStateType = Literal["normal", "disabled", "readonly"]

class EntryMainOptsList(TypedDict):
    bg: NotRequired[str]
    fg: NotRequired[str]
    text: NotRequired[str]
    width: NotRequired[int]
    font: NotRequired[tuple[str, int]]
    justify: NotRequired[str]
    cursor: NotRequired[str]
    readonlybackground: NotRequired[str]
    placeholder_fg: NotRequired[str]
    placeholder: NotRequired[str]
    state: NotRequired[EntryStateType]

@dataclass
class EntryCustomInnerOpts:
    cb: Callable[[Any], None]
    value: str

class EntryCustomOpts(TypedDict):
    placeholder_fg: NotRequired[str]
    placeholder: NotRequired[EntryCustomInnerOpts]
    state: NotRequired[EntryCustomInnerOpts]

@dataclass
class EntryOpts:
    opts: EntryMainOptsList = field(default_factory=EntryMainOptsList)
    _custom: EntryCustomOpts = field(default_factory=EntryCustomOpts)
    cbs: dict[str, Callable[[Any], None]] = field(default_factory=dict)

    def __getitem__(self, key) -> object:
        return getattr(self, key)

    def get_dict(self) -> dict[str, Any]:
        return asdict(self)


class TodoDataType(TypedDict):
    id: NotRequired[str]
    ordering: int
    state: TodoStateType
    title: str
    date: NotRequired[datetime]

