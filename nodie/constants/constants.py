MAX_RECURSION_DEPTH = 100
DANGEROUS_ATTRIBUTES = {
    "onclick",
    "onload",
    "onerror",
    "onmouseover",
    "onmouseout",
    "onkeydown",
    "onkeyup",
    "onkeypress",
    "onfocus",
    "onblur",
    "onchange",
    "onsubmit",
    "onreset",
    "ondblclick",
    "oncontextmenu",
    "oninput",
    "onselect",
    "ondrag",
    "ondrop",
    "onscroll",
}
DANGEROUS_PROTOCOLS = ["javascript:", "data:", "vbscript:", "file:"]
