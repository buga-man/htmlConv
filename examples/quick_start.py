from html_conv import Attributes, HTMLNode, to_html

# Create HTML structure
html_attrs = Attributes({"lang": "en"}, "html")
html = HTMLNode("html", html_attrs, is_self_closed_tag=False)

# Head section
head_attrs = Attributes({}, "head")
head = HTMLNode("head", head_attrs, is_self_closed_tag=False)

title_attrs = Attributes({}, "title")
title = HTMLNode("title", title_attrs, is_self_closed_tag=False)
title.add_child("My Page")
head.add_child(title)

# Body section
body_attrs = Attributes({}, "body")
body = HTMLNode("body", body_attrs, is_self_closed_tag=False)

# Header
header_attrs = Attributes({"class": "header"}, "header")
header = HTMLNode("header", header_attrs, is_self_closed_tag=False)

h1_attrs = Attributes({}, "h1")
h1 = HTMLNode("h1", h1_attrs, is_self_closed_tag=False)
h1.add_child("Welcome to My Website")
header.add_child(h1)

# Main content
main_attrs = Attributes({"class": "main-content"}, "main")
main = HTMLNode("main", main_attrs, is_self_closed_tag=False)

p_attrs = Attributes({}, "p")
p = HTMLNode("p", p_attrs, is_self_closed_tag=False)
p.add_child("This is a simple example of using html-conv library.")
main.add_child(p)

# Footer
footer_attrs = Attributes({"class": "footer"}, "footer")
footer = HTMLNode("footer", footer_attrs, is_self_closed_tag=False)
footer.add_child("© 2024 My Website")

# Assemble the page
body.add_child(header)
body.add_child(main)
body.add_child(footer)

html.add_child(head)
html.add_child(body)

# Generate HTML
page_html = to_html(html)
print(page_html)
