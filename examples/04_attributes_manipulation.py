"""Examples demonstrating attribute manipulation."""

from html_conv import HTMLNode, to_html


def example_global_attributes():
    """Use global HTML attributes."""
    print("=== Global Attributes ===")

    node = HTMLNode.from_dict(
        {
            "tag_name": "div",
            "attributes": {
                "id": "main-content",
                "class": "container primary",
                "title": "Main content area",
                "lang": "en",
                "dir": "ltr",
                "tabindex": "0",
                "role": "main",
                "contenteditable": "true",
                "draggable": "true",
                "hidden": "false",
                "spellcheck": "true",
            },
            "children": ["Content with global attributes"],
        }
    )

    print(to_html(node))
    print()


def example_event_attributes():
    """Use event handler attributes."""
    print("=== Event Handler Attributes ===")

    node = HTMLNode.from_dict(
        {
            "tag_name": "button",
            "attributes": {
                "type": "button",
                "onclick": "handleClick()",
                "onmouseover": "handleHover()",
                "onmouseout": "handleLeave()",
                "onfocus": "handleFocus()",
                "onblur": "handleBlur()",
            },
            "children": ["Interactive Button"],
        }
    )

    print(to_html(node))
    print()


def example_form_attributes():
    """Use form-specific attributes."""
    print("=== Form Attributes ===")

    form = HTMLNode.from_dict(
        {
            "tag_name": "form",
            "attributes": {
                "action": "/submit",
                "method": "post",
                "enctype": "multipart/form-data",
                "autocomplete": "on",
                "novalidate": "false",
            },
            "children": [
                {
                    "tag_name": "input",
                    "attributes": {
                        "type": "text",
                        "name": "username",
                        "placeholder": "Enter username",
                        "required": "true",
                        "minlength": "3",
                        "maxlength": "20",
                        "pattern": "[A-Za-z0-9]+",
                        "autocomplete": "username",
                    },
                    "children": [],
                },
                {
                    "tag_name": "input",
                    "attributes": {
                        "type": "email",
                        "name": "email",
                        "placeholder": "Enter email",
                        "required": "true",
                    },
                    "children": [],
                },
                {
                    "tag_name": "button",
                    "attributes": {"type": "submit"},
                    "children": ["Submit"],
                },
            ],
        }
    )

    print(to_html(form))
    print()


def example_media_attributes():
    """Use media-specific attributes."""
    print("=== Media Attributes ===")

    # Video element
    video = HTMLNode.from_dict(
        {
            "tag_name": "video",
            "attributes": {
                "src": "video.mp4",
                "width": "640",
                "height": "360",
                "controls": "true",
                "autoplay": "false",
                "loop": "false",
                "muted": "false",
                "preload": "metadata",
                "poster": "thumbnail.jpg",
            },
            "children": ["Your browser does not support video."],
        }
    )

    # Audio element
    audio = HTMLNode.from_dict(
        {
            "tag_name": "audio",
            "attributes": {
                "src": "audio.mp3",
                "controls": "true",
                "autoplay": "false",
                "loop": "true",
                "preload": "auto",
            },
            "children": ["Your browser does not support audio."],
        }
    )

    print(to_html(video))
    print()
    print(to_html(audio))
    print()


def example_link_attributes():
    """Use link-specific attributes."""
    print("=== Link Attributes ===")

    node = HTMLNode.from_dict(
        {
            "tag_name": "a",
            "attributes": {
                "href": "https://example.com",
                "target": "_blank",
                "rel": "noopener noreferrer",
                "download": "file.pdf",
                "hreflang": "en",
                "type": "application/pdf",
                "referrerpolicy": "no-referrer",
            },
            "children": ["Download PDF"],
        }
    )

    print(to_html(node))
    print()


def main():
    """Run all attribute manipulation examples."""
    example_global_attributes()
    example_event_attributes()
    example_form_attributes()
    example_media_attributes()
    example_link_attributes()
