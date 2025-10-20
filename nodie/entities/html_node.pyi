from nodie.constants.types import (
    ExternalAttributesType,
    InterpretableDataType,
)
from nodie.entities.attributes import Attributes
from nodie.entities.inline_style_attributes import InlineStyleAttributes

class Children:
    children: list[HTMLNode | str]

    def __init__(self, children: list[HTMLNode | str]) -> None: ...
    def add_child(self, child_node: HTMLNode | str) -> None: ...
    def add_children(self, new_children: tuple[HTMLNode | str, ...]) -> None: ...
    def remove_child(self, child_node_id: str) -> None: ...
    def remove_children(self) -> None: ...

class HTMLNode:
    tag_name: str
    attributes: Attributes
    inline_styles: InlineStyleAttributes
    children: Children
    is_self_closed_tag: bool
    attrs_map_identifier: str

    def __init__(
        self,
        tag_name: str,
        attributes: Attributes,
        is_self_closed_tag: bool,
        inline_styles: InlineStyleAttributes,
        children: Children,
        attrs_map_identifier: str = "default",
    ) -> None: ...
    @property
    def node_id(self) -> str: ...
    def update_node_id(self) -> None: ...
    @classmethod
    def from_dict(
        cls,
        interpretable_data: InterpretableDataType,
        attrs_mapper: ExternalAttributesType | None = None,
        _depth: int = 0,
    ) -> HTMLNode: ...
    def get_children(self) -> list[HTMLNode | str]: ...
    def get_attributes(self) -> dict[str, str]: ...
    @classmethod
    def generate_children(
        cls, children: tuple[InterpretableDataType | str, ...], _depth: int = 0
    ) -> Children: ...
