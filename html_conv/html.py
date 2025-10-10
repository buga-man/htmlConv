from typing import Any

from html_conv.constants.attributes import Attributes
from html_conv.constants.html_tag_mappers import HTML_TAGS


class HTML:
    def __init__(
        self,
        tag_name: str,
        attributes: Attributes,
        is_self_closed_tag: bool,
        children: "tuple[HTML | str, ...]" = (),
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
        self.children = children
        self.is_self_closed_tag = is_self_closed_tag

    @property
    def node_id(self) -> str:
        """Get the unique identifier for this node.

        Returns:
            str: The unique UUID string identifier assigned to this node instance.
        """
        return self._node_id

    @node_id.setter
    def node_id(self, value: str) -> None:
        """Set the unique identifier for this node.

        Updates the node's unique identifier. This setter allows manual assignment
        of a node ID, which can be useful when reconstructing nodes from serialized
        data or when you need to maintain specific ID values across operations.

        Args:
            value (str): The new unique identifier to assign to this node. Should
                be a string value, typically a UUID or other unique identifier format.

        Returns:
            None: This setter modifies the node's ID in place and returns nothing.

        Raises:
            TypeError: If the provided value is not a string.
            ValueError: If the provided value is an empty string.
        """
        if not isinstance(value, str):
            raise TypeError(f"Node ID must be a string, got {type(value).__name__}")
        if not value.strip():
            raise ValueError("Node ID cannot be an empty string")
        self._node_id = value
        self.attributes.update_attribute("id", value)

    def add_child(self, child_node: "HTML | str") -> None:
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
        if not isinstance(child_node, HTML | str):
            raise TypeError(
                f"Child must be Node or str, got {type(child_node).__name__}"
            )
        self.children += (child_node,)

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
            if not (isinstance(child, HTML) and child.node_id == child_node_id)
        )

    def to_html(self) -> str:
        """Convert this HTML node to its complete HTML string representation.

        Generates the full HTML string for this node, including its opening tag,
        attributes, children content, and closing tag. For self-closing tags (like
        img, br, hr), only a single self-closing tag is generated. For regular tags,
        the method creates an opening tag, recursively converts all children to HTML,
        and adds a closing tag.

        Returns:
            str: The complete HTML string representation of this node and all its
                descendants. For self-closing tags, returns a single tag like
                '<img src="..." />'. For regular tags, returns the full structure
                like '<div class="...">content</div>' with all nested children
                rendered as HTML.
        """
        html_attrs = self.attributes.attributes_to_html_string()

        if self.is_self_closed_tag:
            return self.create_self_closing_tag_string(html_attrs)
        return (
            self.create_open_tag_string(html_attrs)
            + "".join(self._child_to_html(child) for child in self.children)
            + self.create_close_tag_string()
        )

    def _child_to_html(self, child: "HTML | str") -> str:
        """Convert a child element to its HTML string representation.

        This private helper method processes individual child elements during HTML
        generation. It handles both string content (which is returned as-is) and
        Node instances (which are recursively converted to HTML using their
        to_html method).

        Args:
            child (Node | str): The child element to convert to HTML. Can be either
                a string representing literal text content, or a Node instance
                representing a nested HTML element that needs to be converted.

        Returns:
            str: The HTML string representation of the child element. For string
                children, returns the string unchanged. For Node children, returns
                the result of calling the child's to_html() method.
        """
        if isinstance(child, str):
            return child
        return child.to_html()

    def create_open_tag_string(self, html_attrs: str) -> str:
        return f"<{self.tag_name} {html_attrs}>"

    def create_close_tag_string(self) -> str:
        """Create an HTML closing tag string for this node.

        Generates the closing HTML tag for this node using the node's tag name.
        The closing tag follows the standard HTML format with a forward slash
        before the tag name and is enclosed in angle brackets.

        Returns:
            str: The HTML closing tag string in the format '</{tag_name}>'.
                For example, if the node's tag_name is 'div', this returns '</div>'.
        """
        return f"</{self.tag_name}>"

    def create_self_closing_tag_string(self, html_attrs: str) -> str:
        return f"<{self.tag_name} {html_attrs}/>"

    @classmethod
    def from_dict(cls, interpretable_data: dict[str, Any]) -> "HTML":
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

        attributes = Attributes(interpretable_data.get("attributes", {}), tag_name)

        children = interpretable_data.get("children", ())

        # Create the Node instance with the provided tag name and attributes
        node = cls(interpretable_data["tag_name"], attributes, is_self_closed_tag)

        child_data: dict[str, Any] | str

        # Process the children of the Node
        for child_data in children:
            if not isinstance(child_data, dict | str):
                raise ValueError(
                    f"Invalid child data type: {type(child_data).__name__}"
                )

            child_node = (
                cls.from_dict(child_data)
                if isinstance(child_data, dict)
                else child_data
            )

            node.add_child(child_node)

        return node
