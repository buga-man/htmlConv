from typing import Any

from html_conv.constants.html_tag_mappers import HTML_TAGS
from html_conv.primitives.attributes import Attributes
from html_conv.primitives.inline_styles import InlineStyleAttributes


class HTMLNode:
    def __init__(
        self,
        tag_name: str,
        attributes: Attributes,
        is_self_closed_tag: bool,
        inline_styles: InlineStyleAttributes,
        children: "tuple[HTMLNode | str, ...]" = (),
    ):
        """Initialize a new HTML node instance.

        Creates a new HTML node with the specified tag name, attributes, and children.
        Each node is assigned a unique identifier (UUID) upon creation. The node can
        represent either a self-closing HTML tag (like img, br, hr) or a regular HTML
        element with opening and closing tags.

        Args:
            tag_name (str): The HTML tag name for this node
                (e.g., 'div', 'span', 'img').
                This determines what HTML element will be generated when converting
                the node to an HTML string.
            attributes (Attributes): An Attributes instance containing the HTML
                attributes for this node (e.g., class, id, style). These attributes
                will be included
                in the generated HTML tag.
            is_self_closed_tag (bool): A flag indicating whether this node represents
                a self-closing HTML tag. If True, the node will generate a self-closing
                tag (e.g., '<img/>'). If False, it will generate opening and closing
                tags (e.g., '<div></div>').
            children (tuple[HTML | str, ...], optional): A tuple of child nodes or text
                content to be nested within this node. Each child can be either another
                HTML instance (for nested elements) or a string (for text content).
                Defaults to an empty tuple if no children are provided.

        Returns:
            None: This is a constructor method that initializes the instance and does
                not return a value.
        """
        self._node_id = attributes.get_unique_id()
        self.tag_name = tag_name
        self.attributes = attributes
        self.inline_styles = inline_styles
        self.children = children
        self.is_self_closed_tag = is_self_closed_tag

    @property
    def node_id(self) -> str:
        """Get the unique identifier for this node.

        Returns:
            str: The unique UUID string identifier assigned to this node instance.
        """
        return self._node_id

    def update_node_id(self) -> None:
        """Update the unique identifier for this node.

        Regenerates the node ID and updates the node's attributes with the new ID.

        Returns:
            None: This method modifies the node's attributes in place
            and returns nothing.
        """
        self._node_id = self.attributes.get_unique_id()

    @classmethod
    def from_dict(cls, interpretable_data: dict[str, Any]) -> "HTMLNode":
        """Create a Node instance from a dictionary containing interpretable data.

        This class method is a static method that takes a dictionary as input and
        constructs a Node instance based on the provided data. The dictionary can
        contain various HTML attributes, tag names, and nested elements. The method
        handles the conversion of string values to their corresponding Node instances
        and constructs the Node tree recursively.

        Args:
            interpretable_data (dict[str, Any]): A dictionary containing interpretable
                data representing HTML elements. The dictionary should have the
                following structure:
                {
                    "tag_name": str,
                    "attributes": dict[str, str],
                    "children": list[dict[str, Any] | str],
                }

        Returns:
            Node: A Node instance constructed from the provided dictionary.

        Raises:
            ValueError: If the dictionary does not contain a valid HTML
                element structure.
        """
        tag_name = interpretable_data.get("tag_name")

        # Check if the dictionary contains required keys
        if tag_name is None or (tag_values := HTML_TAGS.get(tag_name, None)) is None:
            raise ValueError("Dictionary must contain valid 'tag_name' key")

        is_self_closed_tag = tag_values[1]
        raw_attrs = interpretable_data.get("attributes", {})

        inline_styles = cls.create_inline_style_attributes_instance(raw_attrs)
        attributes = Attributes(interpretable_data.get("attributes", {}), tag_name)

        # Create the Node instance with the provided tag name and attributes
        node = cls(
            interpretable_data["tag_name"],
            attributes,
            is_self_closed_tag,
            inline_styles=inline_styles,
        )

        children = interpretable_data.get("children", ())
        node.add_children(cls.generate_children_html(children))

        return node

    def add_child(self, child_node: "HTMLNode | str") -> None:
        """Add a child node or text content to this node.

        Appends a new child to the node's children tuple. The child can be either
        another Node instance (for nested HTML elements) or a string (for text content).
        This method validates the child type and raises a TypeError if an invalid
        type is provided.

        Args:
            child_node (Node | str): The child to add to this node. Can be either
                a Node instance representing a nested HTML element, or a string
                representing text content to be included within this node's HTML output.

        Returns:
            None: This method modifies the node's children in place and returns nothing.

        Raises:
            TypeError: If child_node is not a Node instance or string.
        """
        if not isinstance(child_node, HTMLNode | str):
            raise TypeError(
                f"Child must be Node or str, got {type(child_node).__name__}"
            )
        self.children += (child_node,)

    def add_children(self, new_children: "tuple[HTMLNode | str,...]") -> None:
        """Add multiple child nodes or text content to this node.

        Appends multiple new children to the node's children tuple. The children can
        be either another Node instance (for nested HTML elements) or a string
        (for text content) to be included within this node's HTML output. This method
        validates the child type and raises a TypeError if an invalid type is
        provided.

        Args:
            children (tuple[Node | str,...]): The children to add to this node. Can
                be either a Node instance representing a nested HTML element, or a
                string representing text content to be included within this node's HTML
                output.

        Returns:
            None: This method modifies the node's children in place and returns nothing.

        Raises:
            TypeError: If any child in the children tuple is not a Node instance or
                string.
        """
        self.children += new_children

    def remove_child(self, child_node_id: str) -> None:
        """Remove a child node from this node by its unique identifier.

        Searches through the node's children and removes the first child Node that
        matches the specified node ID. Only Node instances are considered for removal;
        string children are ignored since they don't have node IDs. If no matching
        child node is found, the children tuple remains unchanged.

        Args:
            child_node_id (str): The unique identifier of the child Node to remove.
                This should match the node_id property of the target child node.

        Returns:
            None: This method modifies the node's children in place and returns nothing.
        """
        self.children = tuple(
            child
            for child in self.children
            if not (isinstance(child, HTMLNode) and child.node_id == child_node_id)
        )

    @classmethod
    def generate_children_html(
        cls, children: tuple[dict[str, Any] | str, ...]
    ) -> tuple["HTMLNode | str", ...]:
        children_nodes: list[HTMLNode | str] = []
        for child_data in children:
            if isinstance(child_data, dict):
                children_nodes.append(cls.from_dict(child_data))
            else:
                children_nodes.append(child_data)
        return tuple(children_nodes)

    @staticmethod
    def create_inline_style_attributes_instance(
        raw_attrs: dict[str, str | dict[str, str]],
    ) -> InlineStyleAttributes:
        if "style" not in raw_attrs:
            return InlineStyleAttributes({})

        inline_styles = raw_attrs["style"]

        if isinstance(inline_styles, dict):
            del raw_attrs["style"]
        else:
            raise ValueError("Style attribute must be a dictionary")

        return InlineStyleAttributes(inline_styles)

    def remove_children(self) -> None:
        """Remove all child nodes from this node.

        This method modifies the node's children in place and sets the children
        tuple to an empty tuple.

        Returns:
            None: This method modifies the node's children in place and returns nothing.
        """
        self.children = ()
