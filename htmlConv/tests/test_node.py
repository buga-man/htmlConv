from typing import Any
from htmlConv.node import Node


def test_node_creation_with_unique_uuid():
    node1 = Node("div", {})
    node2 = Node("div", {})

    assert node1.node_id != node2.node_id
    assert isinstance(node1.node_id, str)
    assert len(node1.node_id) == 36  # Standard UUID string length


def test_node_correctly_identifies_self_closing_tags():
    # Test self-closing tag
    img_node = Node("img", {"src": "test.jpg", "alt": "test"})
    assert img_node._Node__is_self_closed_tag  # pyright: ignore[reportAttributeAccessIssue]

    # Test non-self-closing tag
    div_node = Node("div", {"class": "container"})
    assert not div_node._Node__is_self_closed_tag  # pyright: ignore[reportAttributeAccessIssue]

    # Test another self-closing tag
    br_node = Node("br", {})
    assert br_node._Node__is_self_closed_tag  # pyright: ignore[reportAttributeAccessIssue]

    # Test another non-self-closing tag
    p_node = Node("p", {})
    assert not p_node._Node__is_self_closed_tag  # pyright: ignore[reportAttributeAccessIssue]


def test_combine_attributes_properly_formatted():
    node = Node("div", {"class": "container", "id": "main", "data-value": "test"})
    result = node.combine_attributes()

    # Since dict order is preserved in Python 3.7+, we can test the exact format
    expected = "class='container' id='main' data-value='test'"
    assert result == expected


def test_combine_attributes_returns_empty_string_when_no_attributes():
    node = Node("div", {})
    result = node.combine_attributes()
    assert result == ""


def test_update_attribute_existing_with_create_new_false():
    node = Node("div", {"class": "old-value", "id": "test"})

    node.update_attribute("class", "new-value", create_new=False)

    assert node.attributes["class"] == "new-value"
    assert node.attributes["id"] == "test"


def test_update_attribute_creates_new_attribute_when_create_new_is_true():
    node = Node("div", {})

    node.update_attribute("class", "test-class", create_new=True)

    assert node.attributes["class"] == "test-class"
    assert len(node.attributes) == 1


def test_remove_child_removes_specific_child_by_node_id():
    parent = Node("div", {})
    child1 = Node("p", {"id": "first"})
    child2 = Node("span", {"class": "second"})
    child3 = Node("h1", {"title": "third"})

    parent.add_child(child1)
    parent.add_child(child2)
    parent.add_child(child3)

    assert len(parent.children) == 3

    parent.remove_child(child2.node_id)

    assert len(parent.children) == 2
    assert child1 in parent.children
    assert child2 not in parent.children
    assert child3 in parent.children


def test_add_child_adds_node_to_children_tuple():
    parent_node = Node("div", {"class": "parent"})
    child_node = Node("p", {"id": "child"})

    assert len(parent_node.children) == 0

    parent_node.add_child(child_node)

    assert len(parent_node.children) == 1
    assert parent_node.children[0] is child_node


def test_clean_attributes_clears_all_attributes():
    # Arrange
    node = Node("div", {"class": "container", "id": "main", "data-value": "test"})

    # Act
    node.clean_attributes()

    # Assert
    assert node.attributes == {}


def test_update_attribute_should_not_create_new_attribute_when_create_new_false_and_attribute_doesnt_exist():
    node = Node("div", {})

    node.update_attribute("class", "test-class", create_new=False)

    assert "class" not in node.attributes
    assert node.attributes == {}


def test_to_html_returns_self_closing_tag_html_string_when_node_is_self_closing_tag():
    img_node = Node("img", {"src": "test.jpg", "alt": "test image"})

    result = img_node.to_html()

    assert result == "<img src='test.jpg' alt='test image'/>"


def test_to_html_returns_html_string_with_children_content_between_open_and_close_tags_for_non_self_closing_tag():
    parent_node = Node("div", {"class": "container"})
    child_text = "Hello World"
    child_node = Node("p", {"id": "paragraph"})
    child_node.add_child("Some text content")

    parent_node.add_child(child_text)
    parent_node.add_child(child_node)

    result = parent_node.to_html()

    expected = "<div class='container'>Hello World<p id='paragraph'>Some text content</p></div>"
    assert result == expected


def test_to_html_returns_complete_html_string_with_open_and_close_tags_for_non_self_closing_tag_with_no_children():
    node = Node("div", {"class": "container", "id": "main"})

    result = node.to_html()

    expected = "<div class='container' id='main'></div>"
    assert result == expected


def test_to_html_returns_properly_nested_html_when_node_has_multiple_children():
    parent = Node("div", {"class": "container"})
    child1 = Node("p", {"id": "paragraph"})
    child2 = "Some text content"
    child3 = Node("span", {"class": "highlight"})

    parent.add_child(child1)
    parent.add_child(child2)
    parent.add_child(child3)

    result = parent.to_html()

    expected = "<div class='container'><p id='paragraph'></p>Some text content<span class='highlight'></span></div>"
    assert result == expected


def test_to_html_returns_html_string_with_special_characters_in_tag_name_properly_formatted():
    node = Node("custom-tag", {"data-value": "test"})
    child_node = Node("span", {"class": "child"})
    node.add_child(child_node)

    result = node.to_html()

    expected = "<custom-tag data-value='test'><span class='child'></span></custom-tag>"
    assert result == expected


def test_to_html_handles_deeply_nested_children_structure():
    # Create a deeply nested structure: div > ul > li > span > "text"
    span_node = Node("span", {"class": "text-wrapper"})
    span_node.add_child("Hello World")

    li_node = Node("li", {"class": "list-item"})
    li_node.add_child(span_node)

    ul_node = Node("ul", {"id": "main-list"})
    ul_node.add_child(li_node)

    div_node = Node("div", {"class": "container"})
    div_node.add_child(ul_node)

    result = div_node.to_html()

    expected = "<div class='container'><ul id='main-list'><li class='list-item'><span class='text-wrapper'>Hello World</span></li></ul></div>"
    assert result == expected


def test_to_html_returns_html_with_mixed_child_types_including_text_nodes_and_element_nodes():
    parent = Node("div", {"class": "container"})
    child_element = Node("span", {"id": "highlight"})
    text_node = "Hello World"
    another_element = Node("p", {})
    another_text = " and more text"

    parent.add_child(text_node)
    parent.add_child(child_element)
    parent.add_child(another_text)
    parent.add_child(another_element)

    result = parent.to_html()

    expected = "<div class='container'>Hello World<span id='highlight'></span> and more text<p></p></div>"
    assert result == expected


def test_to_html_returns_html_with_proper_tag_ordering_when_children_are_added_in_specific_sequence():
    parent = Node("div", {"class": "wrapper"})
    first_child = Node("h1", {"id": "title"})
    second_child = "Text content"
    third_child = Node("p", {"class": "description"})
    fourth_child = Node("span", {"data-role": "highlight"})

    parent.add_child(first_child)
    parent.add_child(second_child)
    parent.add_child(third_child)
    parent.add_child(fourth_child)

    result = parent.to_html()

    expected = "<div class='wrapper'><h1 id='title'></h1>Text content<p class='description'></p><span data-role='highlight'></span></div>"
    assert result == expected


def test_to_html_handles_empty_children_list():
    node = Node("div", {"class": "container"})

    result = node.to_html()

    expected = "<div class='container'></div>"
    assert result == expected


def test_from_dict_creates_node_with_correct_tag_name_when_dictionary_contains_only_tag_name():
    interpretable_data = {"tag_name": "div"}

    result = Node.from_dict(interpretable_data)

    assert result.tag_name == "div"
    assert result.attributes == {}
    assert result.children == ()
    assert isinstance(result.node_id, str)


def test_from_dict_creates_node_with_attributes_when_dictionary_contains_tag_name_and_attributes():
    # Arrange
    interpretable_data: dict[str, Any] = {
        "tag_name": "div",
        "attributes": {"class": "container", "id": "main"},
    }

    # Act
    result = Node.from_dict(interpretable_data)

    # Assert
    assert result.tag_name == "div"
    assert result.attributes == {"class": "container", "id": "main"}
    assert len(result.children) == 0


def test_from_dict_creates_node_with_string_children_when_dictionary_contains_children_as_list_of_strings():
    interpretable_data: dict[str, Any] = {
        "tag_name": "div",
        "attributes": {"class": "container"},
        "children": ["Hello World", "Some text content", "More text"],
    }

    result = Node.from_dict(interpretable_data)

    assert result.tag_name == "div"
    assert result.attributes == {"class": "container"}
    assert len(result.children) == 3
    assert result.children[0] == "Hello World"
    assert result.children[1] == "Some text content"
    assert result.children[2] == "More text"
    assert all(isinstance(child, str) for child in result.children)


def test_from_dict_creates_node_with_nested_node_children_when_dictionary_contains_children_as_list_of_dictionaries():
    interpretable_data: dict[str, Any] = {
        "tag_name": "div",
        "attributes": {"class": "container"},
        "children": [
            {
                "tag_name": "p",
                "attributes": {"id": "paragraph"},
                "children": ["Some text content"],
            },
            {"tag_name": "span", "attributes": {"class": "highlight"}},
        ],
    }

    result = Node.from_dict(interpretable_data)

    assert result.tag_name == "div"
    assert result.attributes == {"class": "container"}
    assert len(result.children) == 2

    # Check first child (p element)
    first_child = result.children[0]
    assert isinstance(first_child, Node)
    assert first_child.tag_name == "p"
    assert first_child.attributes == {"id": "paragraph"}
    assert len(first_child.children) == 1
    assert first_child.children[0] == "Some text content"

    # Check second child (span element)
    second_child = result.children[1]
    assert isinstance(second_child, Node)
    assert second_child.tag_name == "span"
    assert second_child.attributes == {"class": "highlight"}
    assert len(second_child.children) == 0


def test_from_dict_creates_node_with_mixed_string_and_dictionary_children_when_dictionary_contains_both_types():
    interpretable_data: dict[str, Any] = {
        "tag_name": "div",
        "attributes": {"class": "container"},
        "children": [
            "Hello World",
            {"tag_name": "span", "attributes": {"id": "highlight"}},
            "More text",
            {"tag_name": "p", "attributes": {"class": "paragraph"}},
        ],
    }

    result = Node.from_dict(interpretable_data)

    assert result.tag_name == "div"
    assert result.attributes == {"class": "container"}
    assert len(result.children) == 4
    assert result.children[0] == "Hello World"
    assert isinstance(result.children[1], Node)
    assert result.children[1].tag_name == "span"
    assert result.children[1].attributes == {"id": "highlight"}
    assert result.children[2] == "More text"
    assert isinstance(result.children[3], Node)
    assert result.children[3].tag_name == "p"
    assert result.children[3].attributes == {"class": "paragraph"}


def test_from_dict_recursively_creates_deeply_nested_node_structure_when_dictionary_contains_multiple_levels_of_nested_children():
    interpretable_data: dict[str, Any] = {
        "tag_name": "div",
        "attributes": {"class": "wrapper"},
        "children": [
            {
                "tag_name": "header",
                "attributes": {"id": "main-header"},
                "children": [
                    {
                        "tag_name": "nav",
                        "attributes": {"class": "navigation"},
                        "children": [
                            {
                                "tag_name": "ul",
                                "attributes": {"class": "nav-list"},
                                "children": [
                                    {
                                        "tag_name": "li",
                                        "attributes": {"class": "nav-item"},
                                        "children": [
                                            {
                                                "tag_name": "a",
                                                "attributes": {
                                                    "href": "/home",
                                                    "class": "nav-link",
                                                },
                                                "children": ["Home"],
                                            }
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    }

    result = Node.from_dict(interpretable_data)

    # Assert root level
    assert result.tag_name == "div"
    assert result.attributes == {"class": "wrapper"}
    assert len(result.children) == 1

    # Assert header level
    header_node = result.children[0]
    assert isinstance(header_node, Node)
    assert header_node.tag_name == "header"
    assert header_node.attributes == {"id": "main-header"}
    assert len(header_node.children) == 1

    # Assert nav level
    nav_node = header_node.children[0]
    assert isinstance(nav_node, Node)
    assert nav_node.tag_name == "nav"
    assert nav_node.attributes == {"class": "navigation"}
    assert len(nav_node.children) == 1

    # Assert ul level
    ul_node = nav_node.children[0]
    assert isinstance(ul_node, Node)
    assert ul_node.tag_name == "ul"
    assert ul_node.attributes == {"class": "nav-list"}
    assert len(ul_node.children) == 1

    # Assert li level
    li_node = ul_node.children[0]
    assert isinstance(li_node, Node)
    assert li_node.tag_name == "li"
    assert li_node.attributes == {"class": "nav-item"}
    assert len(li_node.children) == 1

    # Assert a level
    a_node = li_node.children[0]
    assert isinstance(a_node, Node)
    assert a_node.tag_name == "a"
    assert a_node.attributes == {"href": "/home", "class": "nav-link"}
    assert len(a_node.children) == 1
    assert a_node.children[0] == "Home"
