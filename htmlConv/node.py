from typing import Any
from uuid import uuid4
from htmlConv.constants.html_tag_mappers import SELF_CLOSING_TAGS


class Node:
    def __init__(
        self,
        tag_name: str,
        attributes: dict[str, str],
        children: "tuple[Node | str, ...]" = (),
    ):
        """Initialize a new Node instance representing an HTML element.

        Creates a new HTML node with the specified tag name, attributes, and children.
        Each node is assigned a unique identifier and automatically determines if it
        represents a self-closing HTML tag based on the tag name.

        Args:
            tag_name (str): The HTML tag name for this node (e.g., 'div', 'p', 'img').
            attributes (dict[str, str]): A dictionary of HTML attributes where keys are
                attribute names and values are attribute values.
            children (tuple[Node | str, ...], optional): A tuple of child nodes or text
                content. Child nodes can be other Node instances or string literals.
                Defaults to an empty tuple.
        """
        self._node_id = str(uuid4())
        self.tag_name = tag_name
        self.attributes = attributes
        self.children = children
        self.__is_self_closed_tag = tag_name in SELF_CLOSING_TAGS

    @property
    def node_id(self) -> str:
        """Get the unique identifier for this node.

        Returns:
            str: The unique UUID string identifier assigned to this node instance.
        """
        return self._node_id

    def combine_attributes(self) -> str:
        """Combine all node attributes into a single HTML attribute string.

        Converts the node's attributes dictionary into a properly formatted HTML
        attribute string suitable for inclusion in HTML tags. Each attribute is
        formatted as key='value' and multiple attributes are separated by spaces.

        Returns:
            str: A formatted HTML attribute string containing all node attributes,
                or an empty string if no attributes exist. For example, if the node
                has attributes {'class': 'container', 'id': 'main'}, this returns
                "class='container' id='main'".
        """
        combined_attributes = " ".join(
            f"{key}='{value}'" for key, value in self.attributes.items()
        )
        return combined_attributes if combined_attributes else ""

    def update_attribute(
        self, attribute_name: str, new_value: str, create_new: bool = True
    ) -> None:
        """Update or create an HTML attribute for this node.

        Modifies an existing attribute or creates a new one based on the create_new
        parameter. When create_new is True, the attribute will be added regardless
        of whether it already exists. When create_new is False, the attribute will
        only be updated if it already exists in the node's attributes.

        Args:
            attribute_name (str): The name of the HTML attribute to update or create.
            new_value (str): The new value to assign to the specified attribute.
            create_new (bool, optional): Whether to create the attribute if it doesn't
                exist. If True, creates new attributes or updates existing ones. If
                False, only updates attributes that already exist. Defaults to True.

        Returns:
            None: This method modifies the node's attributes in place and returns nothing.
        """
        if create_new:
            self.attributes[attribute_name] = new_value
        else:
            if attribute_name in self.attributes:
                self.attributes[attribute_name] = new_value

    def clean_attributes(self) -> None:
        """Remove all attributes from this node.

        Clears the node's attributes dictionary by setting it to an empty dictionary.
        This effectively removes all HTML attributes that were previously assigned
        to this node, resetting it to have no attributes.

        Returns:
            None: This method modifies the node's attributes in place and returns nothing.
        """
        self.attributes = {}

    def add_child(self, child_node: "Node | str") -> None:
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
        if not isinstance(child_node, (Node, str)):  # pyright: ignore[reportUnnecessaryIsInstance]
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
            if not (isinstance(child, Node) and child.node_id == child_node_id)
        )

    def to_html(self) -> str:
        """Convert this node and all its children to an HTML string representation.

        Generates a complete HTML string for this node, including its opening tag,
        all child content, and closing tag. For self-closing tags (like img, br, hr),
        only a self-closing tag is generated. For regular tags, the method creates
        an opening tag, recursively converts all children to HTML, and adds a closing tag.

        Returns:
            str: A complete HTML string representation of this node and all its
                descendants. For self-closing tags, returns a single self-closing tag.
                For regular tags, returns the opening tag, all child content as HTML,
                and the closing tag concatenated together.
        """
        if self.__is_self_closed_tag:
            return self.create_self_closing_tag_string()
        return (
            self.create_open_tag_string()
            + "".join(self._child_to_html(child) for child in self.children)
            + self.create_close_tag_string()
        )

    def _child_to_html(self, child: "Node | str") -> str:
        """Convert a child element to its HTML string representation.

        This private helper method processes individual child elements during HTML
        generation. It handles both string content (which is returned as-is) and
        Node instances (which are recursively converted to HTML using their to_html method).

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

    def create_open_tag_string(self) -> str:
        """Create an HTML opening tag string for this node.

        Generates the opening HTML tag for this node by combining the tag name
        with any attributes. If the node has attributes, they are included in
        the tag; otherwise, a simple opening tag with just the tag name is created.

        Returns:
            str: The HTML opening tag string. If attributes exist, returns a tag
                in the format '<tag_name attribute1='value1' attribute2='value2'>'.
                If no attributes exist, returns a simple tag in the format '<tag_name>'.
        """
        attributes = self.combine_attributes()
        if attributes:
            return f"<{self.tag_name} {attributes}>"
        return f"<{self.tag_name}>"

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

    def create_self_closing_tag_string(self) -> str:
        """Create an HTML self-closing tag string for this node.

        Generates a self-closing HTML tag for this node by combining the tag name
        with any attributes. Self-closing tags are used for HTML elements that don't
        contain content, such as img, br, hr, input, etc. If the node has attributes,
        they are included in the tag; otherwise, a simple self-closing tag with just
        the tag name is created.

        Returns:
            str: The HTML self-closing tag string. If attributes exist, returns a tag
                in the format '<tag_name attribute1='value1' attribute2='value2'/>'.
                If no attributes exist, returns a simple tag in the format '<tag_name/>'.
        """
        attributes = self.combine_attributes()
        if attributes:
            return f"<{self.tag_name} {attributes}/>"
        return f"<{self.tag_name}/>"

    @classmethod
    def from_dict(cls, interpretable_data: dict[str, Any]) -> "Node":
        """Create a Node instance from a dictionary containing interpretable data.

        This class method is a static method that takes a dictionary as input and
        constructs a Node instance based on the provided data. The dictionary can
        contain various HTML attributes, tag names, and nested elements. The method
        handles the conversion of string values to their corresponding Node instances
        and constructs the Node tree recursively.

        Args:
            interpretable_data (dict[str, Any]): A dictionary containing interpretable
                data representing HTML elements. The dictionary should have the following
                structure:
                {
                    "tag_name": str,
                    "attributes": dict[str, str],
                    "children": list[dict[str, Any] | str],
                }

        Returns:
            Node: A Node instance constructed from the provided dictionary.

        Raises:
            ValueError: If the dictionary does not contain a valid HTML element structure.
        """
        tag_name = interpretable_data.get("tag_name")
        attributes = interpretable_data.get("attributes", {})
        children = interpretable_data.get("children", ())

        # Check if the dictionary contains required keys
        if tag_name is None:
            raise ValueError("Dictionary must contain 'tag_name' key")

        # Create the Node instance with the provided tag name and attributes
        node = cls(interpretable_data["tag_name"], attributes)

        child_data: dict[str, Any] | str

        # Process the children of the Node
        for child_data in children:
            if not isinstance(child_data, (dict, str)):  # pyright: ignore[reportUnnecessaryIsInstance]
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
