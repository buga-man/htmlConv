import re
from typing import Any

from nodie.constants.constants import (
    DANGEROUS_ATTRIBUTES,
    DANGEROUS_PROTOCOLS,
    MAX_RECURSION_DEPTH,
)
from nodie.constants.html_tag_mappers import HTML_TAGS
from nodie.constants.types import ExternalAttributesType, NodeAttributesType
from nodie.entities.attributes import Attributes
from nodie.entities.inline_style_attributes import InlineStyleAttributes
from nodie.exceptions import SecurityError
from nodie.logging_config import get_logger

logger = get_logger(__name__)


class Children:
    def __init__(self, children: list["HTMLNode | str"]) -> None:
        self.children: list[HTMLNode | str] = children

    def add_child(self, child_node: "HTMLNode | str") -> None:
        if not isinstance(child_node, HTMLNode | str):
            raise TypeError(
                f"Child must be Node or str, got {type(child_node).__name__}"
            )
        self.children.append(child_node)

    def add_children(self, new_children: "tuple[HTMLNode | str,...]") -> None:
        self.children.extend(new_children)

    def remove_child(self, child_node_id: str) -> None:
        self.children = [
            child
            for child in self.children
            if not (isinstance(child, HTMLNode) and child.node_id == child_node_id)
        ]

    def remove_children(self) -> None:
        self.children = []


class HTMLNode:
    def __init__(
        self,
        tag_name: str,
        attributes: Attributes,
        is_self_closed_tag: bool,
        inline_styles: InlineStyleAttributes,
        children: Children,
        attrs_map_identifier: str = "default",
    ):
        self._node_id = attributes.get_unique_id()
        self.tag_name = tag_name
        self.attributes = attributes
        self.inline_styles = inline_styles
        self.children = children
        self.is_self_closed_tag = is_self_closed_tag
        self.attrs_map_identifier = attrs_map_identifier

    @property
    def node_id(self) -> str:
        return self._node_id

    def update_node_id(self) -> None:
        self._node_id = self.attributes.get_unique_id()

    @classmethod
    def from_dict(
        cls,
        interpretable_data: NodeAttributesType,
        attrs_mapper: ExternalAttributesType | None = None,
        _depth: int = 0,
    ) -> "HTMLNode":
        # Защита от DoS через глубокую рекурсию
        if _depth > MAX_RECURSION_DEPTH:
            raise SecurityError(
                f"Maximum recursion depth ({MAX_RECURSION_DEPTH}) exceeded. "
                "Possible DoS attack or malformed data."
            )

        tag_name = interpretable_data.get("tag_name")

        if not isinstance(tag_name, str):
            raise TypeError(f"Tag name must be a string, got {type(tag_name).__name__}")

        # Валидация tag_name на безопасность
        validated_tag_name = cls.__validate_tag_name(tag_name)

        # Check if the dictionary contains required keys
        if (
            validated_tag_name is None
            or (tag_values := HTML_TAGS.get(validated_tag_name, None)) is None
        ):
            raise ValueError(f"Invalid or unsupported tag name: '{tag_name}'")

        is_self_closed_tag = tag_values[1]

        raw_attrs, attrs_identifier = cls.__generate_raw_attributes_from_dict(
            interpretable_data, attrs_mapper
        )

        # Валидация атрибутов на безопасность
        safe_raw_attrs = cls.__validate_attributes(raw_attrs, validated_tag_name)

        inline_styles = cls.__create_inline_style_attributes_instance(safe_raw_attrs)
        clean_attrs = cls.__clean_attributes(safe_raw_attrs)

        attributes = Attributes(clean_attrs, validated_tag_name)
        children = interpretable_data.get("children", ())

        if not isinstance(children, tuple | list):
            raise TypeError(
                f"Children must be an iterable, got {type(children).__name__}"
            )

        node = cls(
            validated_tag_name,
            attributes,
            is_self_closed_tag,
            inline_styles=inline_styles,
            attrs_map_identifier=attrs_identifier,
            children=cls.generate_children(children, _depth + 1),
        )

        return node

    def get_children(self) -> list["HTMLNode | str"]:
        return self.children.children

    @classmethod
    def generate_children(
        cls, children: tuple[dict[str, Any] | str, ...], _depth: int = 0
    ) -> Children:
        children_nodes: list[HTMLNode | str] = []
        for child_data in children:
            if isinstance(child_data, dict):
                children_nodes.append(cls.from_dict(child_data, _depth=_depth))
            elif isinstance(child_data, str):
                children_nodes.append(cls.__sanitize_text_content(child_data))
        return Children(children_nodes)

    @staticmethod
    def __validate_tag_name(tag_name: str) -> str:
        """Validate and sanitize tag name.

        Args:
            tag_name: Raw tag name from user input

        Returns:
            Validated tag name

        Raises:
            SecurityError: If tag name contains dangerous characters
        """
        tag_name = tag_name.strip().lower()

        if not re.match(r"^[a-z][a-z0-9-]*", tag_name):
            logger.error("Invalid tag name format: '%s'", tag_name)
            raise SecurityError(
                f"Tag name contains invalid characters: '{tag_name}'. "
                "Only alphanumeric characters and hyphens are allowed."
            )

        if len(tag_name) > 50:
            raise SecurityError(f"Tag name too long: {len(tag_name)} characters")

        return tag_name

    @staticmethod
    def __validate_attributes(attrs: dict[str, Any], tag_name: str) -> dict[str, Any]:
        """Validate and sanitize attributes.

        Args:
            attrs: Raw attributes dictionary
            tag_name: Tag name for context-specific validation

        Returns:
            Validated attributes dictionary
        """
        safe_attrs: dict[str, Any] = {}

        for key, value in attrs.items():
            normalized_key = key.strip().lower()

            if normalized_key in DANGEROUS_ATTRIBUTES:
                logger.warning(
                    "Dangerous attribute '%s' blocked for tag '%s'",
                    normalized_key,
                    tag_name,
                )
                continue

            if not re.match(r"^[a-z][a-z0-9-_]*", normalized_key):
                logger.warning("Invalid attribute name '%s' skipped", normalized_key)
                continue

            if normalized_key == "style":
                safe_attrs[normalized_key] = value
                continue

            if isinstance(value, str):
                safe_value = HTMLNode.__validate_attribute_value(
                    normalized_key, value, tag_name
                )
                if safe_value is not None:
                    safe_attrs[normalized_key] = safe_value
            else:
                logger.warning(
                    "Attribute '%s' has non-string value, skipping", normalized_key
                )

        return safe_attrs

    @staticmethod
    def __validate_attribute_value(
        attr_name: str, value: str, tag_name: str
    ) -> str | None:
        """Validate attribute value for dangerous content.

        Args:
            attr_name: Attribute name
            value: Attribute value to validate
            tag_name: Tag name for context

        Returns:
            Safe value or None if invalid
        """
        lower_value = value.lower()
        for protocol in DANGEROUS_PROTOCOLS:
            if lower_value.startswith(protocol):
                logger.warning(
                    "Dangerous protocol '%s' found in attribute '%s' of tag '%s'",
                    protocol,
                    attr_name,
                    tag_name,
                )
                return None

        if len(value) > 1000:
            logger.warning(
                "Attribute '%s' value too long (%d chars), truncated",
                attr_name,
                len(value),
            )
            return value[:1000]

        return value

    @staticmethod
    def __sanitize_text_content(text: str) -> str:
        """Sanitize text content to prevent XSS attacks.

        Args:
            text: Raw text content

        Returns:
            Sanitized text content
        """
        sanitized = re.sub(r"[<>&]", "", text)
        return sanitized

    @staticmethod
    def __create_inline_style_attributes_instance(
        raw_attrs: NodeAttributesType,
    ) -> InlineStyleAttributes:
        if "style" not in raw_attrs:
            return InlineStyleAttributes({})

        style_attrs = raw_attrs["style"]

        if not isinstance(style_attrs, dict):
            raise ValueError("Style attribute must be a dictionary")

        return InlineStyleAttributes(style_attrs)

    @classmethod
    def __generate_raw_attributes_from_dict(
        cls,
        interpretable_data: dict[str, Any],
        attrs_mapper: dict[str, NodeAttributesType] | None = None,
    ) -> tuple[NodeAttributesType, str]:
        if not attrs_mapper:
            return interpretable_data.get("attributes", {}), "default"

        attrs_identifier = interpretable_data.get("attrs_map_identifier")
        if attrs_identifier is None:
            logger.warning("attrs_map_identifier not found, set 'default'")
            attrs_identifier = "default"

        mapped_attrs: NodeAttributesType = attrs_mapper.get(attrs_identifier, {})
        return mapped_attrs, attrs_identifier

    @classmethod
    def __clean_attributes(
        cls, raw_attrs: dict[str, str | dict[str, str]]
    ) -> dict[str, str]:
        clean_attrs: dict[str, str] = {
            key: value
            for key, value in raw_attrs.items()
            if key != "style" and isinstance(value, str)
        }
        return clean_attrs
