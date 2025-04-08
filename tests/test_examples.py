from anytree import Node, RenderTree

from .helper import eq_


def test_stackoverflow():
    """Example from stackoverflow."""
    udo = Node("Udo")
    marc = Node("Marc", parent=udo)
    Node("Lian", parent=marc)
    dan = Node("Dan", parent=udo)
    Node("Jet", parent=dan)
    Node("Jan", parent=dan)
    joe = Node("Joe", parent=dan)

    eq_(str(udo), "Node('/Udo')")
    eq_(str(joe), "Node('/Udo/Dan/Joe')")

    eq_(
        [f"{pre}{node.name}" for pre, fill, node in RenderTree(udo)],
        [
            "Udo",
            "├── Marc",
            "│   └── Lian",
            "└── Dan",
            "    ├── Jet",
            "    ├── Jan",
            "    └── Joe",
        ],
    )
    eq_(str(dan.children), "(Node('/Udo/Dan/Jet'), Node('/Udo/Dan/Jan'), Node('/Udo/Dan/Joe'))")
