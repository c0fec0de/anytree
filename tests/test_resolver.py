# -*- coding: utf-8 -*-
from enum import IntEnum

from nose.tools import eq_

import anytree as at
from anytree import Node
from anytree import RenderTree
from anytree import Resolver
from helper import assert_raises


def test_get():
    """Get."""
    top = at.Node("top", parent=None)
    sub0 = at.Node("sub0", parent=top)
    sub0sub0 = at.Node("sub0sub0", parent=sub0)
    sub0sub1 = at.Node("sub0sub1", parent=sub0)
    sub1 = at.Node("sub1", parent=top)
    r = at.Resolver('name')
    eq_(r.get(top, "sub0/sub0sub0"), sub0sub0)
    eq_(r.get(sub1, ".."), top)
    eq_(r.get(sub1, "../sub0/sub0sub1"), sub0sub1)
    eq_(r.get(sub1, "."), sub1)
    eq_(r.get(sub1, ""), sub1)
    with assert_raises(at.ChildResolverError,
                       "Node('/top') has no child sub2. Children are: 'sub0', 'sub1'."):
        r.get(top, "sub2")
    eq_(r.get(sub0sub0, "/top"), top)
    eq_(r.get(sub0sub0, "/top/sub0"), sub0)
    with assert_raises(at.ResolverError, "root node missing. root is '/top'."):
        r.get(sub0sub0, "/")
    with assert_raises(at.ResolverError, "unknown root node '/bar'. root is '/top'."):
        r.get(sub0sub0, "/bar")


def test_glob():
    """Wildcard."""
    top = at.Node("top", parent=None)
    sub0 = at.Node("sub0", parent=top)
    sub0sub0 = at.Node("sub0", parent=sub0)
    sub0sub1 = at.Node("sub1", parent=sub0)
    sub0sub1sub0 = at.Node("sub0", parent=sub0sub1)
    at.Node("sub1", parent=sub0sub1)
    sub1 = at.Node("sub1", parent=top)
    sub1sub0 = at.Node("sub0", parent=sub1)
    r = at.Resolver()
    eq_(r.glob(top, "*/*/sub0"), [sub0sub1sub0])

    eq_(r.glob(top, "sub0/sub?"), [sub0sub0, sub0sub1])
    eq_(r.glob(sub1, ".././*"), [sub0, sub1])
    eq_(r.glob(top, "*/*"), [sub0sub0, sub0sub1, sub1sub0])
    eq_(r.glob(top, "*/sub0"), [sub0sub0, sub1sub0])
    with assert_raises(at.ChildResolverError,
                       "Node('/top/sub1') has no child sub1. Children are: 'sub0'."):
        r.glob(top, "sub1/sub1")


def test_glob_cache():
    """Wildcard Cache."""
    root = at.Node("root")
    sub0 = at.Node("sub0", parent=root)
    sub1 = at.Node("sub1", parent=root)
    r = at.Resolver()
    # strip down cache size
    at.resolver._MAXCACHE = 2
    at.Resolver._match_cache.clear()
    eq_(len(at.Resolver._match_cache), 0)
    eq_(r.glob(root, "sub0"), [sub0])
    eq_(len(at.Resolver._match_cache), 1)
    eq_(r.glob(root, "sub1"), [sub1])
    eq_(len(at.Resolver._match_cache), 2)
    eq_(r.glob(root, "sub*"), [sub0, sub1])
    eq_(len(at.Resolver._match_cache), 1)


def test_same_name():
    """Same Name."""
    root = at.Node("root")
    sub0 = at.Node("sub", parent=root)
    sub1 = at.Node("sub", parent=root)
    r = at.Resolver()
    eq_(r.get(root, "sub"), sub0)
    eq_(r.glob(root, "sub"), [sub0, sub1])


def test_enum():
    class Animals(IntEnum):
        Mammal = 1
        Cat = 2
        Dog = 3

    root = Node("ANIMAL")
    mammal = Node(Animals.Mammal, parent=root)
    cat = Node(Animals.Cat, parent=mammal)
    dog = Node(Animals.Dog, parent=mammal)

    r = Resolver()
    eq_(r.glob(root, "/ANIMAL/*"), [mammal])
    eq_(r.glob(root, "/ANIMAL/*/*"), [cat, dog])
