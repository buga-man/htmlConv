from typing import NotRequired, TypedDict, TypeVar

AttrValue = str | int | float | bool

T = TypeVar("T", bound=AttrValue)

ExternalAttributesType = dict[str, dict[str, str | dict[str, str]]]
NodeAttributesType = dict[str, str | dict[str, str]]


# Определение типа для interpretable_data
class InterpretableDataType(TypedDict):
    """Type definition for data that can be interpreted as an HTMLNode.

    Attributes:
        tag_name: HTML tag name (required)
        attributes: Dictionary of HTML attributes (optional)
        children: Tuple or list of child nodes or text content (optional)
        attrs_map_identifier: Identifier for external attribute mapping (optional)
    """

    tag_name: str
    attributes: NotRequired[NodeAttributesType]
    children: NotRequired[
        tuple["InterpretableDataType | str", ...] | list["InterpretableDataType | str"]
    ]
    attrs_map_identifier: NotRequired[str]
