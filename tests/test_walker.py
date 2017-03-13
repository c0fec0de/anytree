from contextlib import contextmanager
from nose.tools import eq_

from anytree import Node
from anytree import WalkError
from anytree import Walker


# hack own assert_raises, because py26 has a diffrent impelmentation
@contextmanager
def assert_raises(exccls, msg):
    try:
        yield
        assert False, "%r not raised" % exccls
    except Exception as exc:
        assert isinstance(exc, exccls), "%r is not a %r" % (exc, exccls)
        eq_(str(exc), msg)



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
    eq_(w.walk(f, f), ([], []))
    eq_(w.walk(f, b), ([], [b]))
    eq_(w.walk(b, f), ([f], []))
    eq_(w.walk(a, f), ([b, f], []))
    eq_(w.walk(b, f), ([f], []))
    eq_(w.walk(h, e), ([i, g, f], [b, d, e]))

    with assert_raises(WalkError, "Node('/a') and Node('/b') are not part of the same tree."):
        w.walk(Node("a"), Node("b"))
