from nodie import HTMLNode
from nodie.logging_config import get_logger

logger = get_logger(__name__)


def node_to_html(child: HTMLNode | str) -> str:
    if isinstance(child, str):
        return child
    return to_html(child)


def to_html(root_node: "HTMLNode", file_path: str | None = None) -> str:
    inline_styles = root_node.inline_styles.to_string()
    html_attrs = inline_styles + " " + root_node.attributes.attributes_to_html_string()
    html: str
    if root_node.is_self_closed_tag:
        html = create_self_closing_tag_string(root_node, html_attrs)
    else:
        html = (
            create_open_tag_string(root_node, html_attrs)
            + "".join(node_to_html(child) for child in root_node.get_children())
            + create_close_tag_string(root_node)
        )

    if file_path is not None:
        save_html(html, file_path)

    return html


def create_open_tag_string(node: HTMLNode, html_attrs: str) -> str:
    tag_template = f"{node.tag_name}"
    if len(html_attrs) > 1:
        tag_template += f"{html_attrs}"
    return f"<{tag_template}>"


def create_close_tag_string(node: HTMLNode) -> str:
    return f"</{node.tag_name}>"


def create_self_closing_tag_string(node: HTMLNode, html_attrs: str) -> str:
    tag_template = f"{node.tag_name}"
    if len(html_attrs) > 1:
        tag_template += f"{html_attrs}"
    return f"<{tag_template}/>"


def save_html(html: str, file_path: str) -> None:
    with open(file_path, "w") as file:
        file.write(html)
        logger.info(f"HTML saved to {file_path} successfully.")
