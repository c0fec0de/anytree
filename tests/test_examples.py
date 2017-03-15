# -*- coding: utf-8 -*-

from nose.tools import eq_

from anytree import Node
from anytree import RenderTree


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

    eq_(["%s%s" % (pre, node.name) for pre, fill, node in RenderTree(udo)], [
        u"Udo",
        u"├── Marc",
        u"│   └── Lian",
        u"└── Dan",
        u"    ├── Jet",
        u"    ├── Jan",
        u"    └── Joe",
    ])
    eq_(str(dan.children),
        "(Node('/Udo/Dan/Jet'), Node('/Udo/Dan/Jan'), Node('/Udo/Dan/Joe'))")
