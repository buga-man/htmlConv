"""Example demonstrating building HTML tables with html-conv library."""

from html_conv import Attributes, HTMLNode, to_html


def create_styled_table() -> HTMLNode:
    """Create a styled table with caption and footer."""
    # Create table
    table_attrs = Attributes({"class": "styled-table", "id": "employee-table"}, "table")
    table = HTMLNode("table", table_attrs, is_self_closed_tag=False)

    # Add caption
    caption_attrs = Attributes({"class": "table-caption"}, "caption")
    caption = HTMLNode("caption", caption_attrs, is_self_closed_tag=False)
    caption.add_child("Employee Information")
    table.add_child(caption)

    # Create colgroup for column styling
    colgroup_attrs = Attributes({}, "colgroup")
    colgroup = HTMLNode("colgroup", colgroup_attrs, is_self_closed_tag=False)

    col_spans = [("1",), ("1",), ("2",)]
    for span in col_spans:
        col_attrs = Attributes({"span": span[0]}, "col")
        col = HTMLNode("col", col_attrs, is_self_closed_tag=True)
        colgroup.add_child(col)

    table.add_child(colgroup)

    # Create header
    thead_attrs = Attributes({}, "thead")
    thead = HTMLNode("thead", thead_attrs, is_self_closed_tag=False)

    tr_head_attrs = Attributes({"class": "header-row"}, "tr")
    tr_head = HTMLNode("tr", tr_head_attrs, is_self_closed_tag=False)

    headers = [
        ("ID", {}),
        ("Name", {}),
        ("Department", {}),
        ("Salary", {"class": "text-right"}),
    ]

    for header_text, header_attrs_dict in headers:
        th_attrs = Attributes(header_attrs_dict, "th")
        th = HTMLNode("th", th_attrs, is_self_closed_tag=False)
        th.add_child(header_text)
        tr_head.add_child(th)

    thead.add_child(tr_head)
    table.add_child(thead)

    # Create body
    tbody_attrs = Attributes({}, "tbody")
    tbody = HTMLNode("tbody", tbody_attrs, is_self_closed_tag=False)

    employees = [
        ("001", "John Doe", "Engineering", "$75,000"),
        ("002", "Jane Smith", "Marketing", "$65,000"),
        ("003", "Bob Johnson", "Sales", "$70,000"),
        ("004", "Alice Williams", "HR", "$60,000"),
    ]

    for i, (emp_id, name, dept, salary) in enumerate(employees):
        row_class = "even-row" if i % 2 == 0 else "odd-row"
        tr_attrs = Attributes({"class": row_class}, "tr")
        tr = HTMLNode("tr", tr_attrs, is_self_closed_tag=False)

        # ID cell
        td_id_attrs = Attributes({"class": "id-cell"}, "td")
        td_id = HTMLNode("td", td_id_attrs, is_self_closed_tag=False)
        td_id.add_child(emp_id)
        tr.add_child(td_id)

        # Name cell
        td_name_attrs = Attributes({}, "td")
        td_name = HTMLNode("td", td_name_attrs, is_self_closed_tag=False)
        td_name.add_child(name)
        tr.add_child(td_name)

        # Department cell
        td_dept_attrs = Attributes({}, "td")
        td_dept = HTMLNode("td", td_dept_attrs, is_self_closed_tag=False)
        td_dept.add_child(dept)
        tr.add_child(td_dept)

        # Salary cell
        td_salary_attrs = Attributes({"class": "text-right"}, "td")
        td_salary = HTMLNode("td", td_salary_attrs, is_self_closed_tag=False)
        td_salary.add_child(salary)
        tr.add_child(td_salary)

        tbody.add_child(tr)

    table.add_child(tbody)

    # Create footer
    tfoot_attrs = Attributes({}, "tfoot")
    tfoot = HTMLNode("tfoot", tfoot_attrs, is_self_closed_tag=False)

    tr_foot_attrs = Attributes({"class": "footer-row"}, "tr")
    tr_foot = HTMLNode("tr", tr_foot_attrs, is_self_closed_tag=False)

    td_total_attrs = Attributes({"colspan": "3", "class": "text-right"}, "td")
    td_total = HTMLNode("td", td_total_attrs, is_self_closed_tag=False)
    td_total.add_child("Total:")
    tr_foot.add_child(td_total)

    td_sum_attrs = Attributes({"class": "text-right total-amount"}, "td")
    td_sum = HTMLNode("td", td_sum_attrs, is_self_closed_tag=False)
    td_sum.add_child("$270,000")
    tr_foot.add_child(td_sum)

    tfoot.add_child(tr_foot)
    table.add_child(tfoot)

    return table


def create_table_from_dict() -> HTMLNode:
    """Create a table using dictionary structure."""
    table_structure = {
        "tag_name": "table",
        "attributes": {"class": "product-table", "border": "1"},
        "children": [
            {
                "tag_name": "caption",
                "attributes": {},
                "children": ["Product Catalog"],
            },
            {
                "tag_name": "thead",
                "attributes": {},
                "children": [
                    {
                        "tag_name": "tr",
                        "attributes": {},
                        "children": [
                            {
                                "tag_name": "th",
                                "attributes": {},
                                "children": ["Product"],
                            },
                            {
                                "tag_name": "th",
                                "attributes": {},
                                "children": ["Price"],
                            },
                            {
                                "tag_name": "th",
                                "attributes": {},
                                "children": ["Stock"],
                            },
                        ],
                    }
                ],
            },
            {
                "tag_name": "tbody",
                "attributes": {},
                "children": [
                    {
                        "tag_name": "tr",
                        "attributes": {},
                        "children": [
                            {
                                "tag_name": "td",
                                "attributes": {},
                                "children": ["Laptop"],
                            },
                            {
                                "tag_name": "td",
                                "attributes": {},
                                "children": ["$999"],
                            },
                            {
                                "tag_name": "td",
                                "attributes": {},
                                "children": ["15"],
                            },
                        ],
                    },
                    {
                        "tag_name": "tr",
                        "attributes": {},
                        "children": [
                            {
                                "tag_name": "td",
                                "attributes": {},
                                "children": ["Mouse"],
                            },
                            {
                                "tag_name": "td",
                                "attributes": {},
                                "children": ["$29"],
                            },
                            {
                                "tag_name": "td",
                                "attributes": {},
                                "children": ["50"],
                            },
                        ],
                    },
                    {
                        "tag_name": "tr",
                        "attributes": {},
                        "children": [
                            {
                                "tag_name": "td",
                                "attributes": {},
                                "children": ["Keyboard"],
                            },
                            {
                                "tag_name": "td",
                                "attributes": {},
                                "children": ["$79"],
                            },
                            {
                                "tag_name": "td",
                                "attributes": {},
                                "children": ["30"],
                            },
                        ],
                    },
                ],
            },
        ],
    }

    return HTMLNode.from_dict(table_structure)


if __name__ == "__main__":
    table_html = create_table_from_dict()
    print(to_html(table_html))

    styled_table = create_styled_table()
    print(to_html(styled_table))
