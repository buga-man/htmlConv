## Core concepts

1. HTMLNode

The HTMLNode class represents an HTML element with:

- tag_name: The HTML tag (e.g., 'div', 'p', 'img')
- attributes: HTML attributes managed by the Attributes class
- children: Nested HTMLNodes or text content
- is_self_closing: Whether the tag is self-closing (e.g., <img />)

2. Attributes

The Attributes class manages HTML attributes with:

- Automatic validation against allowed attributes for each tag
- Support for global attributes (id, class, style, etc.)
- Event handler attributes (onclick, onload, etc.)
- Tag-specific attributes

3. InlineStyles

The InlineStyles class handles CSS inline styles with:

- Validation of CSS property names
- Cleaning and sanitization of values
- Protection against XSS attacks
- Conversion to HTML-ready string format

### Quick Start
#### Creating a Simple HTML Element
```python
from html_conv.node import HTMLNode

# Create a simple div
div = HTMLNode(
    tag_name="div",
    attributes={"class": "container", "id": "main"},
    children=("Hello, World!",)
)

print(div.to_html())
# Output: <div class='container' id='main'>Hello, World!</div>
```

#### Building from Dictionary

```python
from html_conv.node import HTMLNode

html_structure = {
    "tag_name": "div",
    "attributes": {"class": "card"},
    "children": [
        {
            "tag_name": "h2",
            "attributes": {"class": "title"},
            "children": ["Card Title"]
        },
        {
            "tag_name": "p",
            "attributes": {},
            "children": ["Card content goes here."]
        }
    ]
}

node = HTMLNode.from_dict(html_structure)
print(node.to_html())

# <div class='card'>
#     <h2 class='title'>Card Title</h2>
#     <p>Card content goes here.</p>
# </div>
```

### Working with HTML Nodes

#### Creating Nodes

##### Basic Element

```python
from html_conv.node import HTMLNode

# Paragraph with text
paragraph = HTMLNode(
    tag_name="p",
    attributes={"class": "text"},
    children=("This is a paragraph.",)
)
```

##### Self-Closing Element 

```python
# Image tag (automatically detected as self-closing)
image = HTMLNode(
    tag_name="img",
    attributes={
        "src": "image.jpg",
        "alt": "Description"
    }
)

print(image.to_html())
# Output: <img src='image.jpg' alt='Description' />
```

##### Nested Elements

```python
# Create a nested structure
article = HTMLNode(
    tag_name="article",
    attributes={"class": "post"},
    children=(
        HTMLNode(
            tag_name="h1",
            attributes={},
            children=("Article Title",)
        ),
        HTMLNode(
            tag_name="p",
            attributes={},
            children=("Article content...",)
        )
    )
)
```

#### Manipulating Children

##### Adding Children

```python
parent = HTMLNode(tag_name="div", attributes={}, children=())

# Add a single child
child1 = HTMLNode(tag_name="p", attributes={}, children=("First paragraph",))
parent.add_child(child1)

# Add text content
parent.add_child("Some text content")

# Add multiple children
child2 = HTMLNode(tag_name="p", attributes={}, children=("Second paragraph",))
child3 = HTMLNode(tag_name="p", attributes={}, children=("Third paragraph",))
parent.add_children((child2, child3))
```

##### Removing Children

```python
# Remove by index
parent.remove_child(0)  # Removes first child

# Remove by reference
parent.remove_child(child2)

# Clear all children
parent.clear_children()
```

##### Accessing Children

```python
# Get all children
all_children = parent.children

# Iterate over children
for child in parent.children:
    if isinstance(child, HTMLNode):
        print(f"Tag: {child.tag_name}")
    else:
        print(f"Text: {child}")
```

Managing Attributes

Setting Attributes

```python
from html_conv.node import HTMLNode

node = HTMLNode(
    tag_name="div",
    attributes={
        "id": "container",
        "class": "wrapper",
        "data-value": "123"  # Will be filtered out (not a valid attribute)
    }
)

# Note: Invalid attributes are automatically filtered
print(node.attributes.attributes)
# Output: {'id': 'container', 'class': 'wrapper'}
```

Updating Attributes

```python
# Update existing attribute
node.attributes.update_attribute("class", "new-wrapper")

# Add new attribute
node.attributes.update_attribute("title", "Container", create_new=True)

# Update only if exists (won't create new)
node.attributes.update_attribute("data-id", "456", create_new=False)
```

Removing Attributes

```python
# Remove specific attribute
del node.attributes.attributes["class"]

# Clear all attributes
node.attributes.remove_attributes()
```

Getting Attributes

```python
# Get unique ID
element_id = node.attributes.get_unique_id()

# Get all attributes as HTML string
attr_string = node.attributes.attributes_to_html_string()
print(attr_string)
# Output: id='container' class='wrapper'
```

Valid Attributes by Tag

The library automatically validates attributes based on the HTML tag:

```python
# Valid for <a> tag
link = HTMLNode(
    tag_name="a",
    attributes={
        "href": "https://example.com",
        "target": "_blank",
        "rel": "noopener"
    }
)

# Valid for <input> tag
input_field = HTMLNode(
    tag_name="input",
    attributes={
        "type": "text",
        "name": "username",
        "placeholder": "Enter username",
        "required": "required"
    }
)
```

Global Attributes

These attributes work on any HTML element:

```python
element = HTMLNode(
    tag_name="span",
    attributes={
        "id": "unique-id",
        "class": "highlight",
        "style": "color: red;",
        "title": "Tooltip text",
        "lang": "en",
        "dir": "ltr",
        "tabindex": "0",
        "role": "button",
        "aria-label": "Close"
    }
)
```

Event Attributes

```python
button = HTMLNode(
    tag_name="button",
    attributes={
        "onclick": "handleClick()",
        "onmouseover": "showTooltip()",
        "onmouseout": "hideTooltip()"
    },
    children=("Click Me",)
)
```

Styling with InlineStyles

Creating Inline Styles

```python
from html_conv.primitives.inline_styles import InlineStyles

# Create styles object
styles = InlineStyles({
    "color": "red",
    "font-size": "16px",
    "margin": "10px",
    "padding": "5px 10px"
})

# Convert to HTML attribute string
style_attr = styles.to_string()
print(style_attr)
# Output:  style='color: red; font-size: 16px; margin: 10px; padding: 5px 10px;'
```

Using Styles with HTMLNode

```python
from html_conv.node import HTMLNode
from html_conv.primitives.inline_styles import InlineStyles

# Create styled element
styles = InlineStyles({
    "background-color": "#f0f0f0",
    "border": "1px solid #ccc",
    "border-radius": "5px",
    "padding": "20px"
})

div = HTMLNode(
    tag_name="div",
    attributes={"class": "card"},
    children=("Styled content",)
)
```

Updating Styles

```python
styles = InlineStyles({"color": "blue"})

# Add new style
styles.update_style("font-weight", "bold")

# Update existing style
styles.update_style("color", "red")

# Update only if exists
styles.update_style("margin", "10px", create_new=False)
```

Removing Styles

```python
# Remove specific property
styles.remove_style("color")

# Clear all styles
styles.clear_styles()
```

Getting Style Values

```python
# Get specific style value
color = styles.get_style("color")
print(color)  # Output: "red" or ""

# Check if style exists
if styles.get_style("margin"):
    print("Margin is set")
```