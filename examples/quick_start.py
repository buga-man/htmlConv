from typing import Any

from html_сonv import Node

# Create a simple HTML element
div_node = Node("div", {"class": "container"})
div_node.add_child("Hello, World!")

print(div_node.to_html())
# Output: <div class='container'>Hello, World!</div>

# Create from dictionary
data: dict[str, Any] = {
    "tag_name": "div",
    "attributes": {"class": "wrapper"},
    "children": [
        {"tag_name": "h1", "attributes": {"id": "title"}, "children": ["Welcome"]}
    ],
}

node = Node.from_dict(data)
print(node.to_html())
# Output: <div class='wrapper'><h1 id='title'>Welcome</h1></div>
