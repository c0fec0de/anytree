from nose.tools import eq_

from anytree import Node
from anytree import Walker
from anytree import WalkError
from helper import assert_raises


def test_walker():
    """walk test."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)
    w = Walker()
    eq_(w.walk(f, f), ((), f, ()))
    eq_(w.walk(f, b), ((), f, (b,)))
    eq_(w.walk(b, f), ((b,), f, ()))
    eq_(w.walk(a, f), ((a, b), f, ()))
    eq_(w.walk(h, e), ((h, i, g), f, (b, d, e)))
    eq_(w.walk(d, e), ((), d, (e,)))

    with assert_raises(WalkError, "Node('/a') and Node('/b') are not part of the same tree."):
        w.walk(Node("a"), Node("b"))
