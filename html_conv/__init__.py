"""htmlConv - A Python library for converting and manipulating HTML structures.

This library provides a Node-based approach to working with HTML elements,
allowing for easy creation, manipulation, and conversion of HTML structures.
"""

from html_conv.helpers.html_converter import to_html
from html_conv.primitives.html_node import HTMLNode

__version__ = "0.0.2"
__author__ = "Yauheni Buhayeu"
__email__ = "bugaev.zhenka@yandex.by"

__all__ = ["HTMLNode", "to_html"]
