from html_conv import HTMLNode


def node_to_html(child: HTMLNode | str) -> str:
    if isinstance(child, str):
        return child
    return to_html(child)


def to_html(root_node: HTMLNode) -> str:
    inline_styles = root_node.inline_styles.to_string()
    html_attrs = inline_styles + " " + root_node.attributes.attributes_to_html_string()
    html: str
    if root_node.is_self_closed_tag:
        html = create_self_closing_tag_string(root_node, html_attrs)
    else:
        html = (
            create_open_tag_string(root_node, html_attrs)
            + "".join(node_to_html(child) for child in root_node.children)
            + create_close_tag_string(root_node)
        )
    return html


def create_open_tag_string(node: HTMLNode, html_attrs: str) -> str:
    return f"<{node.tag_name} {html_attrs}>"


def create_close_tag_string(node: HTMLNode) -> str:
    return f"</{node.tag_name}>"


def create_self_closing_tag_string(node: HTMLNode, html_attrs: str) -> str:
    return f"<{node.tag_name} {html_attrs}/>"
