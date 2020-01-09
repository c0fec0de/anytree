# -*- coding: utf-8 -*-
"""Test custom node separator."""

import six
from nose.tools import eq_

import anytree as at
from helper import assert_raises


class MyNode(at.Node):

    separator = "|"


def test_render():
    """Render string cast."""
    root = MyNode("root")
    s0 = MyNode("sub0", parent=root)
    MyNode("sub0B", parent=s0)
    MyNode("sub0A", parent=s0)
    MyNode("sub1", parent=root)
    r = at.RenderTree(root)

    expected = u"\n".join([
        u"MyNode('|root')",
        u"├── MyNode('|root|sub0')",
        u"│   ├── MyNode('|root|sub0|sub0B')",
        u"│   └── MyNode('|root|sub0|sub0A')",
        u"└── MyNode('|root|sub1')",
    ])
    if six.PY2:
        eq_(str(r).decode('utf-8'), expected)
    else:
        eq_(str(r), expected)


def test_get():
    """Get."""
    top = MyNode("top", parent=None)
    sub0 = MyNode("sub0", parent=top)
    sub0sub0 = MyNode("sub0sub0", parent=sub0)
    sub0sub1 = MyNode("sub0sub1", parent=sub0)
    sub1 = MyNode("sub1", parent=top)
    r = at.Resolver('name')
    eq_(r.get(top, "sub0|sub0sub0"), sub0sub0)
    eq_(r.get(sub1, ".."), top)
    eq_(r.get(sub1, "..|sub0|sub0sub1"), sub0sub1)
    eq_(r.get(sub1, "."), sub1)
    eq_(r.get(sub1, ""), sub1)
    with assert_raises(at.ChildResolverError,
                       "MyNode('|top') has no child sub2. Children are: 'sub0', 'sub1'."):
        r.get(top, "sub2")
    eq_(r.get(sub0sub0, "|top"), top)
    eq_(r.get(sub0sub0, "|top|sub0"), sub0)
    with assert_raises(at.ResolverError, "root node missing. root is '|top'."):
        r.get(sub0sub0, "|")
    with assert_raises(at.ResolverError, "unknown root node '|bar'. root is '|top'."):
        r.get(sub0sub0, "|bar")


def test_glob():
    """Wildcard."""
    top = MyNode("top", parent=None)
    sub0 = MyNode("sub0", parent=top)
    sub0sub0 = MyNode("sub0", parent=sub0)
    sub0sub1 = MyNode("sub1", parent=sub0)
    sub0sub1sub0 = MyNode("sub0", parent=sub0sub1)
    MyNode("sub1", parent=sub0sub1)
    sub1 = MyNode("sub1", parent=top)
    sub1sub0 = MyNode("sub0", parent=sub1)
    r = at.Resolver()
    eq_(r.glob(top, "*|*|sub0"), [sub0sub1sub0])

    eq_(r.glob(top, "sub0|sub?"), [sub0sub0, sub0sub1])
    eq_(r.glob(sub1, "..|.|*"), [sub0, sub1])
    eq_(r.glob(top, "*|*"), [sub0sub0, sub0sub1, sub1sub0])
    eq_(r.glob(top, "*|sub0"), [sub0sub0, sub1sub0])
    with assert_raises(at.ChildResolverError,
                       "MyNode('|top|sub1') has no child sub1. Children are: 'sub0'."):
        r.glob(top, "sub1|sub1")
