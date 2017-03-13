# -*- coding: utf-8 -*-
from nose.tools import eq_

from anytree import LoopError
from anytree import Node
from anytree import NodeMixin
from anytree import PostOrderIter
from anytree import PreOrderIter


def test_parent_child():
    """A tree parent and child attributes."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1a = Node("sub1A", parent=s1)
    s1b = Node("sub1B", parent=s1)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    eq_(root.parent, None)
    eq_(root.children, tuple([s0, s1]))
    eq_(s0.parent, root)
    eq_(s0.children, tuple([s0b, s0a]))
    eq_(s0b.parent, s0)
    eq_(s0b.children, tuple())
    eq_(s0a.parent, s0)
    eq_(s0a.children, tuple())
    eq_(s1.parent, root)
    eq_(s1.children, tuple([s1a, s1b, s1c]))
    eq_(s1a.parent, s1)
    eq_(s1a.children, tuple())
    eq_(s1b.parent, s1)
    eq_(s1b.children, tuple())
    eq_(s1c.parent, s1)
    eq_(s1c.children, tuple([s1ca]))
    eq_(s1ca.parent, s1c)
    eq_(s1ca.children, tuple())

    # change parent
    s1ca.parent = s0

    eq_(root.parent, None)
    eq_(root.children, tuple([s0, s1]))
    eq_(s0.parent, root)
    eq_(s0.children, tuple([s0b, s0a, s1ca]))
    eq_(s0b.parent, s0)
    eq_(s0b.children, tuple())
    eq_(s0a.parent, s0)
    eq_(s0a.children, tuple())
    eq_(s1.parent, root)
    eq_(s1.children, tuple([s1a, s1b, s1c]))
    eq_(s1a.parent, s1)
    eq_(s1a.children, tuple())
    eq_(s1b.parent, s1)
    eq_(s1b.children, tuple())
    eq_(s1c.parent, s1)
    eq_(s1c.children, tuple())
    eq_(s1ca.parent, s0)
    eq_(s1ca.children, tuple())

    # break tree into two
    s1.parent = None

    eq_(root.parent, None)
    eq_(root.children, tuple([s0]))
    eq_(s0.parent, root)
    eq_(s0.children, tuple([s0b, s0a, s1ca]))
    eq_(s0b.parent, s0)
    eq_(s0b.children, tuple())
    eq_(s0a.parent, s0)
    eq_(s0a.children, tuple())
    eq_(s1.parent, None)
    eq_(s1.children, tuple([s1a, s1b, s1c]))
    eq_(s1a.parent, s1)
    eq_(s1a.children, tuple())
    eq_(s1b.parent, s1)
    eq_(s1b.children, tuple())
    eq_(s1c.parent, s1)
    eq_(s1c.children, tuple())
    eq_(s1ca.parent, s0)
    eq_(s1ca.children, tuple())

    # set to the same
    s1b.parent = s1

    eq_(root.parent, None)
    eq_(root.children, tuple([s0]))
    eq_(s0.parent, root)
    eq_(s0.children, tuple([s0b, s0a, s1ca]))
    eq_(s0b.parent, s0)
    eq_(s0b.children, tuple())
    eq_(s0a.parent, s0)
    eq_(s0a.children, tuple())
    eq_(s1.parent, None)
    eq_(s1.children, tuple([s1a, s1b, s1c]))
    eq_(s1a.parent, s1)
    eq_(s1a.children, tuple())
    eq_(s1b.parent, s1)
    eq_(s1b.children, tuple())
    eq_(s1c.parent, s1)
    eq_(s1c.children, tuple())
    eq_(s1ca.parent, s0)
    eq_(s1ca.children, tuple())


def test_recursion_detection():
    """Recursion detection."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)

    # try recursion
    try:
        root.parent = root
    except LoopError as exc:
        eq_(str(exc), "Cannot set parent. Node('/root') cannot be parent of itself.")
    else:
        assert False
    try:
        root.parent = s0a
    except LoopError as exc:
        eq_(str(exc), (
            "Cannot set parent. "
            "Node('/root') is parent of Node('/root/sub0/sub0A')."))
    else:
        assert False


def test_repr():
    """Node representation."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s1 = Node("sub1", parent=root, foo=42, bar="c0fe")

    eq_(repr(root), "Node('/root')")
    eq_(repr(s0), "Node('/root/sub0')")
    eq_(repr(s1), "Node('/root/sub1', bar='c0fe', foo=42)")


def test_anchestors():
    """Node.anchestors."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    eq_(root.anchestors, tuple())
    eq_(s0.anchestors, tuple([root]))
    eq_(s0b.anchestors, tuple([root, s0]))
    eq_(s0a.anchestors, tuple([root, s0]))
    eq_(s1ca.anchestors, tuple([root, s1, s1c]))


def test_descendants():
    """Node.descendants."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    eq_(root.descendants, tuple([s0, s0b, s0a, s1, s1c, s1ca]))
    eq_(s1.descendants, tuple([s1c, s1ca]))
    eq_(s1c.descendants, tuple([s1ca]))
    eq_(s1ca.descendants, tuple())


def test_root():
    """Node.root."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    eq_(root.root, root)
    eq_(s0.root, root)
    eq_(s0b.root, root)
    eq_(s0a.root, root)
    eq_(s1.root, root)
    eq_(s1c.root, root)
    eq_(s1ca.root, root)


def test_siblings():
    """Node.siblings."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    eq_(root.siblings, tuple())
    eq_(s0.siblings, tuple([s1]))
    eq_(s0b.siblings, tuple([s0a]))
    eq_(s0a.siblings, tuple([s0b]))
    eq_(s1.siblings, tuple([s0]))
    eq_(s1c.siblings, tuple())
    eq_(s1ca.siblings, tuple())


def test_is_leaf():
    """Node.is_leaf."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    eq_(root.is_leaf, False)
    eq_(s0.is_leaf, False)
    eq_(s0b.is_leaf, True)
    eq_(s0a.is_leaf, True)
    eq_(s1.is_leaf, False)
    eq_(s1c.is_leaf, False)
    eq_(s1ca.is_leaf, True)


def test_is_root():
    """Node.is_root."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    eq_(root.is_root, True)
    eq_(s0.is_root, False)
    eq_(s0b.is_root, False)
    eq_(s0a.is_root, False)
    eq_(s1.is_root, False)
    eq_(s1c.is_root, False)
    eq_(s1ca.is_root, False)


def test_height():
    """Node.height."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    eq_(root.height, 3)
    eq_(s0.height, 1)
    eq_(s0b.height, 0)
    eq_(s0a.height, 0)
    eq_(s1.height, 2)
    eq_(s1c.height, 1)
    eq_(s1ca.height, 0)


def test_depth():
    """Node.depth."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    eq_(root.depth, 0)
    eq_(s0.depth, 1)
    eq_(s0b.depth, 2)
    eq_(s0a.depth, 2)
    eq_(s1.depth, 1)
    eq_(s1c.depth, 2)
    eq_(s1ca.depth, 3)


def test_parent():
    """Parent attribute."""
    foo = NodeMixin()
    assert foo.parent is None


def test_pre_order_iter():
    """Pre-Order Iterator."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)

    result = [node.name for node in PreOrderIter(f)]
    expected = ['f', 'b', 'a', 'd', 'c', 'e', 'g', 'i', 'h']
    eq_(result, expected)


def test_post_order_iter():
    """Post-Order Iterator."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)

    result = [node.name for node in PostOrderIter(f)]
    expected = ['a', 'c', 'e', 'd', 'b', 'h', 'i', 'g', 'f']
    eq_(result, expected)


def test_anyname():
    """Support any type as name."""
    myroot = Node([1, 2, 3])
    Node('/foo', parent=myroot)
    eq_(str(myroot), "Node('/[1, 2, 3]')")
