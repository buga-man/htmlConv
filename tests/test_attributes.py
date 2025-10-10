from html_conv.attributes import Attributes
from html_conv.constants import html_tag_mappers


def test_attributes_to_html_string_empty_attributes() -> None:
    """Test that attributes_to_html_string returns empty string
    when attributes dictionary is empty."""
    attrs = Attributes({}, "div")
    result = attrs.attributes_to_html_string()
    assert result == ""


def test_attributes_to_html_string_multiple_attributes() -> None:
    """Test that multiple attributes are formatted correctly with single quotes."""
    attrs = Attributes(
        {"class": "container", "id": "main", "data-value": "test"}, "div"
    )
    result = attrs.attributes_to_html_string()

    # Since dict order is preserved in Python 3.7+, we can check the exact string
    # or we can check that all attributes are present
    assert "class='container'" in result
    assert "id='main'" in result
    assert "data-value='test'" not in result


def test_clean_attributes() -> None:
    """Test that clean_attributes sets attributes to empty dictionary."""
    attrs = Attributes({"class": "container", "id": "main"}, "div")
    attrs.clean_attributes()
    assert attrs.attributes == {}


def test_update_attribute_create_new_true() -> None:
    """Test that update_attribute creates a new attribute when create_new is True."""
    attrs = Attributes({"class": "container"}, "div")

    attrs.update_attribute("data-test", "value", create_new=True)

    assert "data-test" in attrs.attributes
    assert attrs.attributes["data-test"] == "value"


def test_update_attribute_doesnt_create_when_create_new_false_and_attribute_mis() -> (
    None
):
    """Test that update_attribute does not create a new attribute when create_new
    is False and the attribute does not exist."""
    attrs = Attributes({"id": "test-id", "class": "container"}, "div")

    attrs.update_attribute("data-custom", "value", create_new=False)

    assert "data-custom" not in attrs.attributes
    assert attrs.attributes == {"id": "test-id", "class": "container"}


def test_update_attribute_updates_existing_attribute_when_create_new_is_false() -> None:
    # Arrange
    attrs = Attributes({"class": "old-value", "id": "test-id"}, "div")

    # Act
    attrs.update_attribute("class", "new-value", create_new=False)

    # Assert
    assert attrs.attributes["class"] == "new-value"


def test_introspect_attributes_filters_invalid_attributes() -> None:
    """Test that introspect_attributes filters out invalid attributes
    and keeps only valid ones."""
    tag_name = "div"
    attributes = {
        "class": "container",
        "id": "main",
        "invalid_attr": "should_be_removed",
        "data-custom": "should_be_removed",
        "style": "color: red",
    }

    result = Attributes.introspect_attributes(tag_name, attributes)

    assert "class" in result
    assert "id" in result
    assert "style" in result
    assert "invalid_attr" not in result
    assert "data-custom" not in result
    assert result["class"] == "container"
    assert result["id"] == "main"
    assert result["style"] == "color: red"


def test_combine_all_possible_attributes() -> None:
    """Test that combine_all_possible_attributes correctly combines global, event,
    and tag-specific attributes."""

    # Test with a tag that has specific attributes (e.g., 'img')
    result = Attributes.combine_all_possible_attributes("img")

    # Verify that global attributes are included
    assert "class" in result
    assert "id" in result
    assert "style" in result

    # Verify that event attributes are included
    assert "onclick" in result
    assert "onload" in result

    # Verify that tag-specific attributes for 'img' are included
    assert "src" in result
    assert "alt" in result
    assert "width" in result
    assert "height" in result

    # Test with a tag that has no specific attributes (e.g., 'div')
    result_div = Attributes.combine_all_possible_attributes("div")

    # Verify that global and event attributes are still included
    assert "class" in result_div
    assert "onclick" in result_div

    # Verify the result contains all expected attribute types
    expected_count = (
        len(html_tag_mappers.GLOBAL_ATTRIBUTES)
        + len(html_tag_mappers.EVENT_ATTRIBUTES)
        + len(html_tag_mappers.HTML_TAGS["img"][0])
    )
    assert len(result) == expected_count
