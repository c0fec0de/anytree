from anytree import LevelGroupOrderIter
from anytree import LevelOrderIter
from anytree import Node
from nose.tools import eq_


def test_levelorder():
    """LevelOrderIter."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)

    eq_(list(LevelOrderIter(f)), [f, b, g, a, d, i, c, e, h])


def test_levelgrouporder():
    """LevelGroupOrderIter."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)

    eq_(list(LevelGroupOrderIter(f)),
        [(f,), (b, g), (a, d, i), (c, e, h)])
