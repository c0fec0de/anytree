import anytree


def test_render_str():
    """Render string cast."""
    root = anytree.Node("root")
    s0 = anytree.Node("sub0", parent=root)
    anytree.Node("sub0B", parent=s0)
    anytree.Node("sub0A", parent=s0)
    anytree.Node("sub1", parent=root)

    r = anytree.RenderTree(root)
    assert str(r).splitlines() == [
        "Node('/root')",
        "├── Node('/root/sub0')",
        "│   ├── Node('/root/sub0/sub0B')",
        "│   └── Node('/root/sub0/sub0A')",
        "└── Node('/root/sub1')",
    ]

    r = anytree.RenderTree(root, childiter=lambda nodes: [n for n in nodes if len(n.name) < 5])
    assert str(r).splitlines() == [
        "Node('/root')",
        "├── Node('/root/sub0')",
        "└── Node('/root/sub1')",
    ]


def test_render_repr():
    """Render representation."""
    root = anytree.Node("root")
    anytree.Node("sub", parent=root)
    r = anytree.RenderTree(root)

    assert repr(r) == "RenderTree(Node('/root'), style=ContStyle(), childiter=<class 'list'>)"


def test_render():
    """Rendering."""
    root = anytree.Node("root", lines=["c0fe", "c0de"])
    s0 = anytree.Node("sub0", parent=root, lines=["ha", "ba"])
    s0b = anytree.Node("sub0B", parent=s0, lines=["1", "2", "3"])
    s0a = anytree.Node("sub0A", parent=s0, lines=["a", "b"])
    s1 = anytree.Node("sub1", parent=root, lines=["Z"])

    r = anytree.RenderTree(root, style=anytree.DoubleStyle)
    result = [(pre, node) for pre, _, node in r]
    assert result == [
        ("", root),
        ("╠══ ", s0),
        ("║   ╠══ ", s0b),
        ("║   ╚══ ", s0a),
        ("╚══ ", s1),
    ]

    def multi(root):
        for pre, fill, node in anytree.RenderTree(root):
            yield f"{pre}{node.lines[0]}", node
            for line in node.lines[1:]:
                yield f"{fill}{line}", node

    assert list(multi(root)) == [
        ("c0fe", root),
        ("c0de", root),
        ("├── ha", s0),
        ("│   ba", s0),
        ("│   ├── 1", s0b),
        ("│   │   2", s0b),
        ("│   │   3", s0b),
        ("│   └── a", s0a),
        ("│       b", s0a),
        ("└── Z", s1),
    ]


def test_maxlevel():
    root = anytree.Node("root", lines=["c0fe", "c0de"])
    s0 = anytree.Node("sub0", parent=root, lines=["ha", "ba"])
    s0b = anytree.Node("sub0B", parent=s0, lines=["1", "2", "3"])
    s0a = anytree.Node("sub0A", parent=s0, lines=["a", "b"])
    s1 = anytree.Node("sub1", parent=root, lines=["Z"])

    r = anytree.RenderTree(root, maxlevel=2)
    result = [(pre, node) for pre, _, node in r]
    assert result == [
        ("", root),
        ("├── ", s0),
        ("└── ", s1),
    ]


def test_asciistyle():
    style = anytree.AsciiStyle()
    assert style.vertical == "|   "
    assert style.cont == "|-- "
    assert style.end == "+-- "


def test_contstyle():
    style = anytree.ContStyle()
    assert style.vertical == "\u2502   "
    assert style.cont == "\u251c\u2500\u2500 "
    assert style.end == "\u2514\u2500\u2500 "


def test_controundstyle():
    style = anytree.ContRoundStyle()
    assert style.vertical == "\u2502   "
    assert style.cont == "\u251c\u2500\u2500 "
    assert style.end == "\u2570\u2500\u2500 "


def test_doublestyle():
    style = anytree.DoubleStyle()
    assert style.vertical == "\u2551   "
    assert style.cont == "\u2560\u2550\u2550 "
    assert style.end == "\u255a\u2550\u2550 "


def test_by_attr():
    """By attr."""
    root = anytree.Node("root", lines=["root"])
    s0 = anytree.Node("sub0", parent=root, lines=["su", "b0"])
    anytree.Node("sub0B", parent=s0, lines=["sub", "0B"])
    anytree.Node("sub0A", parent=s0)
    anytree.Node("sub1", parent=root, lines=["sub1"])

    assert anytree.RenderTree(root).by_attr().splitlines() == [
        "root",
        "├── sub0",
        "│   ├── sub0B",
        "│   └── sub0A",
        "└── sub1",
    ]
    assert anytree.RenderTree(root).by_attr("lines").splitlines() == [
        "root",
        "├── su",
        "│   b0",
        "│   ├── sub",
        "│   │   0B",
        "│   └── ",
        "└── sub1",
    ]
    assert anytree.RenderTree(root).by_attr(lambda node: ":".join(node.name)).splitlines() == [
        "r:o:o:t",
        "├── s:u:b:0",
        "│   ├── s:u:b:0:B",
        "│   └── s:u:b:0:A",
        "└── s:u:b:1",
    ]


def test_repr():
    """Repr."""

    class ReprNode(anytree.Node):
        def __repr__(self):
            return f"{self.name}\n{self.name}"

    root = ReprNode("root", lines=["root"])
    s0 = ReprNode("sub0", parent=root, lines=["su", "b0"])
    ReprNode("sub0B", parent=s0, lines=["sub", "0B"])
    ReprNode("sub0A", parent=s0)
    ReprNode("sub1", parent=root, lines=["sub1"])

    bystr = str(anytree.RenderTree(root)).splitlines()
    byident = anytree.RenderTree(root).by_attr(lambda node: node).splitlines()
    assert bystr == byident
