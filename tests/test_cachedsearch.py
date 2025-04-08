from anytree import CountError, Node
from anytree.cachedsearch import find, find_by_attr, findall, findall_by_attr

from .helper import assert_raises, eq_


def test_findall():
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)

    eq_(findall(f, filter_=lambda node: node.name in ("a", "b")), (b, a))
    eq_(findall(f, filter_=lambda node: d in node.path), (d, c, e))
    with assert_raises(
        CountError,
        ("Expecting at least 4 elements, but found 3. (Node('/f/b/d'), Node('/f/b/d/c'), Node('/f/b/d/e'))"),
    ):
        findall(f, filter_=lambda node: d in node.path, mincount=4)
    with assert_raises(
        CountError,
        ("Expecting 2 elements at maximum, but found 3. (Node('/f/b/d'), Node('/f/b/d/c'), Node('/f/b/d/e'))"),
    ):
        findall(f, filter_=lambda node: d in node.path, maxcount=2)


def test_findall_by_attr():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    Node("c", parent=d)
    Node("e", parent=d)

    eq_(findall_by_attr(f, "d"), (d,))
    with assert_raises(CountError, ("Expecting at least 1 elements, but found 0.")):
        findall_by_attr(f, "z", mincount=1)


def test_find():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    Node("c", parent=d)
    Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    Node("h", parent=i)

    eq_(find(f, lambda n: n.name == "d"), d)
    eq_(find(f, lambda n: n.name == "z"), None)
    with assert_raises(
        CountError,
        (
            "Expecting 1 elements at maximum, but found 5. "
            "(Node('/f/b'), Node('/f/b/a'), Node('/f/b/d'), Node('/f/b/d/c'), Node('/f/b/d/e'))"
        ),
    ):
        find(f, lambda n: b in n.path)


def test_find_by_attr():
    f = Node("f")
    b = Node("b", parent=f)
    Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d, foo=4)
    Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    Node("h", parent=i)

    eq_(find_by_attr(f, "d"), d)
    eq_(find_by_attr(f, name="foo", value=4), c)
    eq_(find_by_attr(f, name="foo", value=8), None)
