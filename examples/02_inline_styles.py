"""Examples demonstrating inline style attributes."""

from html_conv import HTMLNode, to_html


def example_simple_styles():
    """Apply simple inline styles."""
    print("=== Simple Inline Styles ===")

    node = HTMLNode.from_dict(
        {
            "tag_name": "div",
            "attributes": {
                "class": "styled-box",
                "style": {"color": "blue", "font-size": "16px", "margin": "10px"},
            },
            "children": ["Styled content"],
        }
    )

    print(to_html(node))
    print()


def example_complex_styles():
    """Apply complex inline styles."""
    print("=== Complex Inline Styles ===")

    node = HTMLNode.from_dict(
        {
            "tag_name": "div",
            "attributes": {
                "style": {
                    "display": "flex",
                    "flex-direction": "column",
                    "justify-content": "center",
                    "align-items": "center",
                    "background-color": "#f0f0f0",
                    "border": "2px solid #333",
                    "border-radius": "8px",
                    "padding": "20px",
                    "box-shadow": "0 4px 6px rgba(0,0,0,0.1)",
                    "transition": "all 0.3s ease",
                }
            },
            "children": ["Flexbox container"],
        }
    )

    print(to_html(node))
    print()


def example_typography_styles():
    """Apply typography-related styles."""
    print("=== Typography Styles ===")

    node = HTMLNode.from_dict(
        {
            "tag_name": "p",
            "attributes": {
                "style": {
                    "font-family": "Arial, sans-serif",
                    "font-size": "18px",
                    "font-weight": "bold",
                    "line-height": "1.6",
                    "letter-spacing": "0.5px",
                    "text-align": "justify",
                    "text-decoration": "underline",
                    "text-transform": "uppercase",
                    "color": "#333",
                }
            },
            "children": ["Styled typography"],
        }
    )

    print(to_html(node))
    print()


def example_layout_styles():
    """Apply layout-related styles."""
    print("=== Layout Styles ===")

    node = HTMLNode.from_dict(
        {
            "tag_name": "div",
            "attributes": {
                "style": {
                    "position": "relative",
                    "width": "100%",
                    "max-width": "1200px",
                    "height": "500px",
                    "margin": "0 auto",
                    "padding": "20px",
                    "overflow": "hidden",
                    "z-index": "10",
                }
            },
            "children": ["Layout container"],
        }
    )

    print(to_html(node))
    print()


def main():
    """Run all inline style examples."""
    example_simple_styles()
    example_complex_styles()
    example_typography_styles()
    example_layout_styles()


if __name__ == "__main__":
    main()
