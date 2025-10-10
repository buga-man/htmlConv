import pytest

from html_conv import HTMLNode
from html_conv.attributes import Attributes


def test_create_html_node_with_valid_tag_and_empty_children() -> None:
    """Test creating an HTMLNode instance with valid tag name, attributes,
    and empty children tuple."""
    tag_name = "div"
    attributes = Attributes({"class": "container", "id": "main"}, tag_name)
    is_self_closed_tag = False

    node = HTMLNode(tag_name, attributes, is_self_closed_tag)

    assert node.tag_name == "div"
    assert node.attributes == attributes
    assert node.is_self_closed_tag is False
    assert node.children == ()
    assert node.node_id == "main"


def test_create_self_closed_tag_html_node() -> None:
    """Test creating a self-closed tag HTMLNode with is_self_closed_tag set to True."""
    tag_name = "img"
    attributes = Attributes({"src": "image.jpg", "alt": "Test image"}, tag_name)
    is_self_closed_tag = True

    node = HTMLNode(tag_name, attributes, is_self_closed_tag)

    assert node.tag_name == "img"
    assert node.is_self_closed_tag is True
    assert node.children == ()
    assert node.attributes.attributes == {"src": "image.jpg", "alt": "Test image"}


def test_should_generate_unique_node_id_when_initializing() -> None:
    attributes1 = Attributes({"id": "test-id-1"}, "div")
    attributes2 = Attributes({"id": "test-id-2"}, "div")

    node1 = HTMLNode("div", attributes1, False)
    node2 = HTMLNode("div", attributes2, False)

    assert node1.node_id == "test-id-1"
    assert node2.node_id == "test-id-2"
    assert node1.node_id != node2.node_id


def test_update_node_id() -> None:
    """Test that update_node_id regenerates the node ID from attributes."""
    # Create initial attributes with an id
    initial_attrs = Attributes({"id": "initial-id"}, "div")
    node = HTMLNode("div", initial_attrs, False)

    # Store the initial node_id
    initial_node_id = node.node_id
    assert initial_node_id == "initial-id"

    # Update the id attribute in the attributes object
    node.attributes.update_attribute("id", "updated-id")

    # Call update_node_id to regenerate the node_id
    node.update_node_id()

    # Verify that node_id has been updated
    assert node.node_id == "updated-id"
    assert node.node_id != initial_node_id


def test_from_dict_creates_html_node_with_nested_children() -> None:
    """Test that from_dict creates HTMLNode with valid tag_name,
    attributes, and nested children."""
    interpretable_data = {
        "tag_name": "div",
        "attributes": {"class": "container", "id": "main"},
        "children": (
            "Some text",
            {
                "tag_name": "span",
                "attributes": {"class": "highlight"},
                "children": ("Nested text",),
            },
            "More text",
        ),
    }

    node = HTMLNode.from_dict(interpretable_data)

    assert node.tag_name == "div"
    assert node.attributes.attributes == {"class": "container", "id": "main"}
    assert len(node.children) == 3
    assert node.children[0] == "Some text"
    assert isinstance(node.children[1], HTMLNode)
    assert node.children[1].tag_name == "span"
    assert node.children[1].attributes.attributes == {"class": "highlight"}
    assert node.children[1].children[0] == "Nested text"
    assert node.children[2] == "More text"


def test_from_dict_raises_value_error_for_invalid_tag_name() -> None:
    """Test that from_dict raises ValueError when tag_name is invalid or missing."""

    # Test with missing tag_name
    invalid_data_missing = {"attributes": {"class": "test"}, "children": []}

    with pytest.raises(
        ValueError, match="Dictionary must contain valid 'tag_name' key"
    ):
        HTMLNode.from_dict(invalid_data_missing)

    # Test with None tag_name
    invalid_data_none: dict[str, None | dict | list] = {
        "tag_name": None,
        "attributes": {"class": "test"},
        "children": [],
    }

    with pytest.raises(
        ValueError, match="Dictionary must contain valid 'tag_name' key"
    ):
        HTMLNode.from_dict(invalid_data_none)

    # Test with invalid tag_name (not in HTML_TAGS)
    invalid_data_unknown = {
        "tag_name": "invalidtag",
        "attributes": {"class": "test"},
        "children": [],
    }

    with pytest.raises(
        ValueError, match="Dictionary must contain valid 'tag_name' key"
    ):
        HTMLNode.from_dict(invalid_data_unknown)


def test_add_child_single_node() -> None:
    """Test adding a single child HTMLNode to the children tuple."""
    parent_attrs = Attributes({"id": "parent"}, "div")
    parent_node = HTMLNode("div", parent_attrs, False, ())

    child_attrs = Attributes({"id": "child"}, "span")
    child_node = HTMLNode("span", child_attrs, False, ())

    parent_node.add_child(child_node)

    assert len(parent_node.children) == 1
    assert parent_node.children[0] == child_node
    assert isinstance(parent_node.children[0], HTMLNode)


def test_add_child_single_string() -> None:
    """Test adding a single string to the children tuple."""
    parent_attrs = Attributes({"id": "parent"}, "div")
    parent_node = HTMLNode("div", parent_attrs, False, ())

    text_content = "Hello, World!"
    parent_node.add_child(text_content)

    assert len(parent_node.children) == 1
    assert parent_node.children[0] == text_content
    assert isinstance(parent_node.children[0], str)


def test_add_child_multiple_times() -> None:
    """Test adding multiple children one at a time using add_child."""
    parent_attrs = Attributes({"id": "parent"}, "div")
    parent_node = HTMLNode("div", parent_attrs, False, ())

    child1_attrs = Attributes({"id": "child1"}, "span")
    child1 = HTMLNode("span", child1_attrs, False, ())

    child2 = "Text content"

    parent_node.add_child(child1)
    parent_node.add_child(child2)

    assert len(parent_node.children) == 2
    assert parent_node.children[0] == child1
    assert parent_node.children[1] == child2


def test_remove_child_by_node_id() -> None:
    """Test that remove_child removes a child node by matching node_id."""
    # Create parent node
    parent_attrs = Attributes({"id": "parent"}, "div")
    parent_node = HTMLNode("div", parent_attrs, False)

    # Create child nodes
    child1_attrs = Attributes({"id": "child1"}, "span")
    child1 = HTMLNode("span", child1_attrs, False)

    child2_attrs = Attributes({"id": "child2"}, "span")
    child2 = HTMLNode("span", child2_attrs, False)

    child3_attrs = Attributes({"id": "child3"}, "span")
    child3 = HTMLNode("span", child3_attrs, False)

    # Add children to parent
    parent_node.add_children((child1, child2, child3))

    # Verify all children are present
    assert len(parent_node.children) == 3
    assert child1 in parent_node.children
    assert child2 in parent_node.children
    assert child3 in parent_node.children

    # Remove child2
    parent_node.remove_child(child2.node_id)

    # Verify child2 is removed and others remain
    assert len(parent_node.children) == 2
    assert child1 in parent_node.children  # type: ignore
    assert child2 not in parent_node.children
    assert child3 in parent_node.children
