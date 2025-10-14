from typing import TypeVar

AttrValue = str | int | float | bool
T = TypeVar("T", bound=AttrValue)
