from html_сonv.constants import html_tag_mappers


def introspect_attributes(
    tag_name: str, attributes: dict[str, str], is_self_closed: bool
) -> dict[str, str]:
    cleaned_attrs = clean_attrs_names(
        tag_name, tuple(attributes.keys()), is_self_closed
    )
    return {key: value for key, value in attributes.items() if key in cleaned_attrs}


def clean_attrs_names(
    tag_name: str, attributes: tuple[str, ...], is_self_closed: bool
) -> tuple[str, ...]:
    clean_attrs = []
    all_possible_attrs = combile_all_possible_attributes(tag_name, is_self_closed)
    for attr_name in attributes:
        if attr_name in all_possible_attrs:
            clean_attrs.append(attr_name)
        else:
            print(f"Unknown attribute '{attr_name}' for tag '{tag_name}'.")
    return tuple(clean_attrs)


def combile_all_possible_attributes(
    tag_name: str, is_self_closed: bool
) -> tuple[str, ...]:
    main_mapper: dict[str, tuple[str, ...]] = (
        html_tag_mappers.SELF_CLOSING_TAGS
        if is_self_closed
        else html_tag_mappers.HTML_TAGS
    )
    main_attrs = tuple(main_mapper.get(tag_name, {}))

    return (
        main_attrs
        + tuple(html_tag_mappers.GLOBAL_ATTRIBUTES)
        + tuple(html_tag_mappers.EVENT_ATTRIBUTES)
    )
