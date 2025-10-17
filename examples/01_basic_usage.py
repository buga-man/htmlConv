"""Basic usage examples demonstrating core functionality."""

from html_conv import HTMLNode, to_html


def example_simple_element() -> None:
    """Create a simple HTML element."""
    print("=== Simple Element ===")

    # Create a simple paragraph
    node = HTMLNode.from_dict(
        {
            "tag_name": "p",
            "attributes": {"class": "intro"},
            "children": ["Hello, World!"],
        }
    )

    print(to_html(node))
    print()


def example_nested_structure() -> None:
    """Create nested HTML structure."""
    print("=== Nested Structure ===")

    node = HTMLNode.from_dict(
        {
            "tag_name": "div",
            "attributes": {"class": "container"},
            "children": [
                {
                    "tag_name": "h1",
                    "attributes": {"id": "title"},
                    "children": ["Welcome"],
                },
                {
                    "tag_name": "p",
                    "attributes": {},
                    "children": ["This is a paragraph."],
                },
            ],
        }
    )

    print(to_html(node))
    print()


def example_self_closing_tags() -> None:
    """Demonstrate self-closing tags."""
    print("=== Self-Closing Tags ===")

    # Image tag
    img = HTMLNode.from_dict(
        {
            "tag_name": "img",
            "attributes": {
                "src": "image.jpg",
                "alt": "Description",
                "width": "300",
                "height": "200",
            },
            "children": [],
        }
    )

    # Line break
    br = HTMLNode.from_dict({"tag_name": "br", "attributes": {}, "children": []})

    # Horizontal rule
    hr = HTMLNode.from_dict({"tag_name": "hr", "attributes": {}, "children": []})

    print(to_html(img))
    print(to_html(br))
    print(to_html(hr))
    print()


def main() -> None:
    """Run all basic examples."""
    example_simple_element()
    example_nested_structure()
    example_self_closing_tags()


if __name__ == "__main__":
    main()
