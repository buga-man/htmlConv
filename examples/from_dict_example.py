"""Example demonstrating building HTML from dictionary structure."""

from html_conv import HTMLNode, to_html


def main() -> None:
    """Create HTML structure from dictionary."""
    # Define a complete page structure
    page_structure = {
        "tag_name": "html",
        "attributes": {"lang": "en"},
        "children": [
            {
                "tag_name": "head",
                "attributes": {},
                "children": [
                    {
                        "tag_name": "title",
                        "attributes": {},
                        "children": ["My Blog Post"],
                    }
                ],
            },
            {
                "tag_name": "body",
                "attributes": {"class": "blog-page"},
                "children": [
                    {
                        "tag_name": "article",
                        "attributes": {"class": "post"},
                        "children": [
                            {
                                "tag_name": "h1",
                                "attributes": {"class": "post-title"},
                                "children": ["Getting Started with html-conv"],
                            },
                            {
                                "tag_name": "p",
                                "attributes": {"class": "post-meta"},
                                "children": ["Published on January 1, 2024"],
                            },
                            {
                                "tag_name": "div",
                                "attributes": {"class": "post-content"},
                                "children": [
                                    {
                                        "tag_name": "p",
                                        "attributes": {
                                            "style": {
                                                "font-weight": "bold",
                                                "text-decoration": "underline",
                                            }
                                        },
                                        "children": [
                                            "html-conv is a Python library for "
                                            "building HTML structures programmatically."
                                        ],
                                    },
                                    {
                                        "tag_name": "p",
                                        "attributes": {},
                                        "children": [
                                            "It provides a clean, object-oriented "
                                            "approach to HTML generation."
                                        ],
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
        ],
    }

    # Convert dictionary structure to HTML
    html_output = to_html(HTMLNode.from_dict(page_structure))
    print(html_output)


if __name__ == "__main__":
    main()
