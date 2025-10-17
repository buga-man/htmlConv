"""Examples demonstrating dynamic children manipulation."""

from html_conv import HTMLNode, to_html


def example_add_child():
    """Add children dynamically."""
    print("=== Adding Children Dynamically ===")

    # Create parent node
    parent = HTMLNode.from_dict(
        {"tag_name": "ul", "attributes": {"class": "list"}, "children": []}
    )

    # Add children one by one
    for i in range(1, 4):
        child = HTMLNode.from_dict(
            {"tag_name": "li", "attributes": {}, "children": [f"Item {i}"]}
        )
        parent.children.add_child(child)

    print(to_html(parent))
    print()


def example_add_multiple_children():
    """Add multiple children at once."""
    print("=== Adding Multiple Children ===")

    parent = HTMLNode.from_dict(
        {
            "tag_name": "div",
            "attributes": {"class": "container"},
            "children": [
                {"tag_name": "h2", "attributes": {}, "children": ["Initial heading"]}
            ],
        }
    )

    # Create multiple children
    new_children = tuple(
        [
            HTMLNode.from_dict(
                {"tag_name": "p", "attributes": {}, "children": [f"Paragraph {i}"]}
            )
            for i in range(1, 4)
        ]
    )

    parent.children.add_children(new_children)

    print(to_html(parent))
    print()


def example_remove_child():
    """Remove specific child by ID."""
    print("=== Removing Child by ID ===")

    # Create parent with children
    parent = HTMLNode.from_dict(
        {
            "tag_name": "div",
            "attributes": {},
            "children": [
                {
                    "tag_name": "p",
                    "attributes": {"id": "para1"},
                    "children": ["First paragraph"],
                },
                {
                    "tag_name": "p",
                    "attributes": {"id": "para2"},
                    "children": ["Second paragraph"],
                },
                {
                    "tag_name": "p",
                    "attributes": {"id": "para3"},
                    "children": ["Third paragraph"],
                },
            ],
        }
    )

    print("Before removal:")
    print(to_html(parent))

    # Get the node_id of the second child
    second_child = parent.get_children()[1]
    if isinstance(second_child, HTMLNode):
        parent.children.remove_child(second_child.node_id)

    print("\nAfter removing second paragraph:")
    print(to_html(parent))
    print()


def example_clear_children():
    """Remove all children."""
    print("=== Clearing All Children ===")

    parent = HTMLNode.from_dict(
        {
            "tag_name": "div",
            "attributes": {"class": "content"},
            "children": [
                {"tag_name": "h1", "attributes": {}, "children": ["Title"]},
                {"tag_name": "p", "attributes": {}, "children": ["Content"]},
            ],
        }
    )

    print("Before clearing:")
    print(to_html(parent))

    parent.children.remove_children()

    print("\nAfter clearing:")
    print(to_html(parent))
    print()


def example_mixed_children():
    """Mix text and node children."""
    print("=== Mixed Text and Node Children ===")

    parent = HTMLNode.from_dict(
        {"tag_name": "p", "attributes": {}, "children": ["This is "]}
    )

    # Add emphasis node
    em_node = HTMLNode.from_dict(
        {"tag_name": "em", "attributes": {}, "children": ["emphasized"]}
    )
    parent.children.add_child(em_node)

    # Add more text
    parent.children.add_child(" text with ")

    # Add strong node
    strong_node = HTMLNode.from_dict(
        {"tag_name": "strong", "attributes": {}, "children": ["bold"]}
    )
    parent.children.add_child(strong_node)

    # Add final text
    parent.children.add_child(" content.")

    print(to_html(parent))
    print()


def main():
    """Run all dynamic children examples."""
    example_add_child()
    example_add_multiple_children()
    example_remove_child()
    example_clear_children()
    example_mixed_children()


if __name__ == "__main__":
    main()
