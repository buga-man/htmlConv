import pytest

from nodie import HTMLNode
from nodie.constants.types import InterpretableDataType
from nodie.exceptions import SecurityError


def test_from_dict_raises_security_error_when_tag_name_contains_special_symbols() -> (
    None
):
    # Arrange
    interpretable_data: InterpretableDataType = {
        "tag_name": "div@#$%",
        "attributes": {},
        "children": (),
    }

    # Act & Assert
    with pytest.raises(SecurityError):
        HTMLNode.from_dict(interpretable_data)


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


def test_from_dict_raises_security_error_when_tag_name_not_in_html_tags() -> None:
    # Arrange
    interpretable_data: InterpretableDataType = {
        "tag_name": "customtag",
        "attributes": {},
        "children": (),
    }

    # Act & Assert
    with pytest.raises(SecurityError) as exc_info:
        HTMLNode.from_dict(interpretable_data)

    assert "Invalid or unsupported tag name: 'customtag'" in str(exc_info.value)


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


def test_from_dict_filters_dangerous_attributes_from_list() -> None:
    # Arrange
    interpretable_data: InterpretableDataType = {
        "tag_name": "div",
        "attributes": {
            "class": "safe-class",
            "onmouseover": "malicious()",
            "onfocus": "badCode()",
            "id": "safe-id",
            "onblur": "danger()",
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
    assert "onmouseover" not in attrs_dict
    assert "onfocus" not in attrs_dict
    assert "onblur" not in attrs_dict


def test_validate_attribute_value_returns_none_for_dangerous_protocols() -> None:
    # Arrange
    interpretable_data: InterpretableDataType = {
        "tag_name": "a",
        "attributes": {
            "href": "javascript:void(0)",
            "src": "data:text/html,<script>alert('XSS')</script>",
            "action": "vbscript:msgbox('XSS')",
        },
        "children": (),
    }

    # Act
    node = HTMLNode.from_dict(interpretable_data)

    # Assert
    node_attributes = node.get_attributes()
    assert "href" not in node_attributes
    assert "src" not in node_attributes
    assert "action" not in node_attributes


def test_escape_html_special_characters_in_text_content() -> None:
    # Arrange
    interpretable_data: InterpretableDataType = {
        "tag_name": "div",
        "children": (
            "Hello <script>alert('xss')</script> World",
            "Text with & ampersand",
            "<>Test<>",
            "Quote \" and apostrophe '",
        ),
    }

    # Act
    node = HTMLNode.from_dict(interpretable_data)
    children = node.get_children()

    # Assert
    assert len(children) == 4
    assert (
        children[0] == "Hello &lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt; World"
    )
    assert children[1] == "Text with &amp; ampersand"
    assert children[2] == "&lt;&gt;Test&lt;&gt;"
    assert children[3] == "Quote &quot; and apostrophe &#x27;"
