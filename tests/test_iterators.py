from anytree import (
    LevelGroupOrderIter,
    LevelOrderGroupIter,
    LevelOrderIter,
    Node,
    PostOrderIter,
    PreOrderIter,
    ZigZagGroupIter,
)

from .helper import eq_


def test_preorder():
    """PreOrderIter."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)
    k = Node("k", parent=a)
    o = Node("o", parent=k)
    m = Node("m", parent=e)

    eq_(list(PreOrderIter(f)), [f, b, a, k, o, d, c, e, m, g, i, h])
    eq_(list(PreOrderIter(f, maxlevel=0)), [])
    eq_(list(PreOrderIter(f, maxlevel=2)), [f, b, g])
    eq_(list(PreOrderIter(f, maxlevel=3)), [f, b, a, d, g, i])
    eq_(list(PreOrderIter(f, maxlevel=4)), [f, b, a, k, d, c, e, g, i, h])
    eq_(list(PreOrderIter(f, maxlevel=f.height + 1)), list(PreOrderIter(f)))
    eq_(list(PreOrderIter(f, filter_=lambda n: n.name not in ("e", "g"))), [f, b, a, k, o, d, c, m, i, h])
    eq_(list(PreOrderIter(f, stop=lambda n: n.name == "d")), [f, b, a, k, o, g, i, h])

    it = PreOrderIter(f)
    eq_(next(it), f)
    eq_(next(it), b)
    eq_(list(it), [a, k, o, d, c, e, m, g, i, h])


def test_postorder():
    """PostOrderIter."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)

    eq_(list(PostOrderIter(f)), [a, c, e, d, b, h, i, g, f])
    eq_(list(PostOrderIter(f, maxlevel=0)), [])
    eq_(list(PostOrderIter(f, maxlevel=3)), [a, d, b, i, g, f])
    eq_(list(PostOrderIter(f, filter_=lambda n: n.name not in ("e", "g"))), [a, c, d, b, h, i, f])
    eq_(list(PostOrderIter(f, stop=lambda n: n.name == "d")), [a, b, h, i, g, f])

    it = PostOrderIter(f)
    eq_(next(it), a)
    eq_(next(it), c)
    eq_(list(it), [e, d, b, h, i, g, f])


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
    eq_(list(LevelOrderIter(f, maxlevel=0)), [])
    eq_(list(LevelOrderIter(f, maxlevel=3)), [f, b, g, a, d, i])
    eq_(list(LevelOrderIter(f, filter_=lambda n: n.name not in ("e", "g"))), [f, b, a, d, i, c, h])
    eq_(list(LevelOrderIter(f, stop=lambda n: n.name == "d")), [f, b, g, a, i, h])

    it = LevelOrderIter(f)
    eq_(next(it), f)
    eq_(next(it), b)
    eq_(list(it), [g, a, d, i, c, e, h])


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

    eq_(list(LevelGroupOrderIter(f)), [(f,), (b, g), (a, d, i), (c, e, h)])
    eq_(list(LevelGroupOrderIter(f, maxlevel=0)), [])
    eq_(list(LevelGroupOrderIter(f, maxlevel=3)), [(f,), (b, g), (a, d, i)])
    eq_(list(LevelGroupOrderIter(f, filter_=lambda n: n.name not in ("e", "g"))), [(f,), (b,), (a, d, i), (c, h)])
    eq_(list(LevelGroupOrderIter(f, stop=lambda n: n.name == "d")), [(f,), (b, g), (a, i), (h,)])

    it = LevelGroupOrderIter(f)
    eq_(next(it), (f,))
    eq_(next(it), (b, g))
    eq_(list(it), [(a, d, i), (c, e, h)])


def test_levelordergroup():
    """LevelOrderGroupIter."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)

    eq_(list(LevelOrderGroupIter(f)), [(f,), (b, g), (a, d, i), (c, e, h)])
    eq_(list(LevelOrderGroupIter(f, maxlevel=0)), [])
    eq_(list(LevelOrderGroupIter(f, maxlevel=3)), [(f,), (b, g), (a, d, i)])
    eq_(list(LevelOrderGroupIter(f, filter_=lambda n: n.name not in ("e", "g"))), [(f,), (b,), (a, d, i), (c, h)])
    eq_(list(LevelOrderGroupIter(f, stop=lambda n: n.name == "d")), [(f,), (b, g), (a, i), (h,)])

    it = LevelOrderGroupIter(f)
    eq_(next(it), (f,))
    eq_(next(it), (b, g))
    eq_(list(it), [(a, d, i), (c, e, h)])


def test_zigzaggroup():
    """ZigZagGroupIter."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)

    eq_(list(ZigZagGroupIter(f)), [(f,), (g, b), (a, d, i), (h, e, c)])
    eq_(list(ZigZagGroupIter(f, maxlevel=0)), [])
    eq_(list(ZigZagGroupIter(f, maxlevel=3)), [(f,), (g, b), (a, d, i)])
    eq_(list(ZigZagGroupIter(f, filter_=lambda n: n.name not in ("e", "g"))), [(f,), (b,), (a, d, i), (h, c)])
    eq_(list(ZigZagGroupIter(f, stop=lambda n: n.name == "d")), [(f,), (g, b), (a, i), (h,)])

    it = ZigZagGroupIter(f)
    eq_(next(it), (f,))
    eq_(next(it), (g, b))
    eq_(list(it), [(a, d, i), (h, e, c)])
