import pytest

from nodie import HTMLNode
from nodie.constants.constants import MAX_RECURSION_DEPTH
from nodie.constants.types import InterpretableDataType
from nodie.exceptions import SecurityError


def test_from_dict_raises_security_error_when_tag_name_exceeds_max_length() -> None:
    # Arrange

    long_tag_name = "a" * 51  # 51 characters, exceeds max of 50
    interpretable_data: InterpretableDataType = {
        "tag_name": long_tag_name,
        "attributes": {},
        "children": (),
    }

    with pytest.raises(SecurityError) as exc_info:
        HTMLNode.from_dict(interpretable_data)

    assert "Tag name too long" in str(exc_info.value)
    assert "51 characters" in str(exc_info.value)


def test_from_dict_raises_security_error_when_tag_name_contains_invalid_chars() -> None:
    interpretable_data: InterpretableDataType = {
        "tag_name": "div<script>",
        "attributes": {},
        "children": (),
    }

    with pytest.raises(SecurityError) as exc_info:
        HTMLNode.from_dict(interpretable_data)

    assert "Invalid or unsupported tag name: 'div<script>'" in str(exc_info.value)


def test_raise_security_error_recursion_depth_max_during_nested_children_creation() -> (
    None
):
    nested_data: InterpretableDataType = {"tag_name": "div", "children": ()}
    current: InterpretableDataType = nested_data

    for _ in range(MAX_RECURSION_DEPTH + 2):
        child: InterpretableDataType = {"tag_name": "div", "children": ()}
        current["children"] = (child,)
        current = child

    with pytest.raises(SecurityError) as exc_info:
        HTMLNode.from_dict(nested_data)

    assert "Maximum recursion depth" in str(exc_info.value)
    assert "exceeded" in str(exc_info.value)


def test_validate_attributes_blocks_dangerous_attributes() -> None:
    # Arrange
    interpretable_data: InterpretableDataType = {
        "tag_name": "div",
        "attributes": {
            "class": "safe-class",
            "onclick": "alert('XSS')",
            "onerror": "malicious()",
            "id": "safe-id",
            "onload": "dangerous()",
        },
    }

    # Act
    node = HTMLNode.from_dict(interpretable_data)

    # Assert
    attrs_dict = node.get_attributes()
    assert "class" in attrs_dict
    assert attrs_dict["class"] == "safe-class"
    assert "id" in attrs_dict
    assert attrs_dict["id"] == "safe-id"
    assert "onclick" not in attrs_dict
    assert "onerror" not in attrs_dict
    assert "onload" not in attrs_dict


def test_from_dict_blocks_dangerous_protocols_in_attribute_values() -> None:
    # Arrange
    interpretable_data: InterpretableDataType = {
        "tag_name": "a",
        "attributes": {
            "href": "javascript:alert('XSS')",
            "src": "data:text/html,<script>alert('XSS')</script>",
            "onclick": "javascript:void(0)",
        },
        "children": (),
    }

    # Act
    node = HTMLNode.from_dict(interpretable_data)

    # Assert
    assert node.tag_name == "a"
    # Dangerous protocols should be blocked, so these attributes should not be present
    node_attributes = node.get_attributes()
    assert "href" not in node_attributes
    assert "src" not in node_attributes
    assert "onclick" not in node_attributes


def test_sanitize_text_content_removes_dangerous_characters() -> None:
    # Arrange
    interpretable_data: InterpretableDataType = {
        "tag_name": "div",
        "children": (
            "Hello <script>alert('xss')</script> World",
            "Text with & ampersand",
            "<>Test<>",
        ),
    }

    # Act
    node = HTMLNode.from_dict(interpretable_data)
    children = node.get_children()
    # Assert
    assert len(children) == 3
    assert children[0] == "Hello scriptalert('xss')/script World"
    assert children[1] == "Text with  ampersand"
    assert children[2] == "Test"


def test_from_dict_raises_type_error_when_children_is_not_tuple_or_list() -> None:
    interpretable_data: InterpretableDataType = {
        "tag_name": "div",
        "attributes": {},
        "children": "invalid_children_type",  # type: ignore
    }

    try:
        HTMLNode.from_dict(interpretable_data)
        raise AssertionError("Expected TypeError to be raised")
    except TypeError as e:
        assert "Children must be an iterable" in str(e)


def test_from_dict_raises_type_error_when_tag_name_is_not_string() -> None:
    interpretable_data: InterpretableDataType = {
        "tag_name": 123,  # type: ignore
        "attributes": {},
    }

    try:
        HTMLNode.from_dict(interpretable_data)
        raise AssertionError("Expected TypeError was not raised")
    except TypeError as e:
        assert "Tag name must be a string" in str(e)
        assert "got int" in str(e)


def test_from_dict_raises_value_error_when_style_attribute_is_not_dictionary() -> None:
    interpretable_data: InterpretableDataType = {
        "tag_name": "div",
        "attributes": {"style": "color: red;"},
    }

    try:
        HTMLNode.from_dict(interpretable_data)
        raise AssertionError("Expected ValueError to be raised")
    except ValueError as e:
        assert str(e) == "Style attribute must be a dictionary"
