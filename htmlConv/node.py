from uuid import uuid4
from htmlConv.constants.html_tag_mappers import SELF_CLOSING_TAGS


class Node:
    def __init__(
        self,
        tag_name: str,
        attributes: dict[str, str],
        children: tuple["Node", ...] = (),
    ):
        self._node_id = str(uuid4())
        self.tag_name = tag_name
        self.attributes = attributes
        self.children = children
        self.__is_self_closed_tag = tag_name in SELF_CLOSING_TAGS

    @property
    def node_id(self) -> str:
        return self._node_id

    def combine_attributes(self) -> str:
        combined_attributes = " ".join(
            f"{key}='{value}'" for key, value in self.attributes.items()
        )
        return combined_attributes if combined_attributes else ""

    def update_attribute(
        self, attribute_name: str, new_value: str, create_new: bool = True
    ) -> None:
        if create_new:
            self.attributes[attribute_name] = new_value
        else:
            if attribute_name in self.attributes:
                self.attributes[attribute_name] = new_value

    def clean_attributes(self) -> None:
        self.attributes = {}

    def add_child(self, child_node: "Node") -> None:
        self.children += (child_node,)

    def remove_child(self, child_node_id: str) -> None:
        self.children = tuple(
            child for child in self.children if child.node_id != child_node_id
        )

    def to_html(self) -> str:
        if self.__is_self_closed_tag:
            return self.create_self_closing_tag_string()
        return (
            self.create_open_tag_string()
            + "".join(child.to_html() for child in self.children)
            + self.create_close_tag_string()
        )

    def create_open_tag_string(self) -> str:
        return f"<{self.tag_name} {self.combine_attributes()}>"

    def create_close_tag_string(self) -> str:
        return f"</{self.tag_name}>"

    def create_self_closing_tag_string(self) -> str:
        return f"<{self.tag_name} {self.combine_attributes()}/>"
