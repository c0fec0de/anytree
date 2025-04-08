from enum import IntEnum

from pytest import raises

import anytree as at
from anytree import Node, Resolver

from .helper import assert_raises


def test_get():
    """Get."""
    top = at.Node("top", parent=None)
    sub0 = at.Node("sub0", parent=top)
    sub0sub0 = at.Node("sub0sub0", parent=sub0)
    sub0sub1 = at.Node("sub0sub1", parent=sub0)
    sub1 = at.Node("sub1", parent=top)
    r = at.Resolver("name")
    assert r.get(top, "sub0/sub0sub0") == sub0sub0
    assert r.get(sub1, "..") == top
    assert r.get(sub1, "../") == top
    assert r.get(sub1, "../.") == top
    assert r.get(sub1, "../sub0/sub0sub1") == sub0sub1
    assert r.get(sub1, ".") == sub1
    assert r.get(sub1, "") == sub1
    with assert_raises(at.ChildResolverError, "Node('/top') has no child sub2. Children are: 'sub0', 'sub1'."):
        r.get(top, "sub2")
    assert r.get(sub0sub0, "/top") == top
    assert r.get(sub0sub0, "/top/sub0") == sub0
    with assert_raises(at.RootResolverError, "Cannot go above root node Node('/top')"):
        r.get(top, "..")
    with assert_raises(at.ResolverError, "root node missing. root is '/top'."):
        r.get(sub0sub0, "/")
    with assert_raises(at.ResolverError, "unknown root node '/bar'. root is '/top'."):
        r.get(sub0sub0, "/bar")


def test_get_relaxed():
    """Get in relaxed mode."""
    top = at.Node("top", parent=None)
    sub0 = at.Node("sub0", parent=top)
    sub0sub0 = at.Node("sub0sub0", parent=sub0)
    sub0sub1 = at.Node("sub0sub1", parent=sub0)
    sub1 = at.Node("sub1", parent=top)
    r = at.Resolver("name", relax=True)
    assert r.get(top, "sub0/sub0sub0") == sub0sub0
    assert r.get(sub1, "..") == top
    assert r.get(sub1, "../") == top
    assert r.get(sub1, "../.") == top
    assert r.get(sub1, "../sub0/sub0sub1") == sub0sub1
    assert r.get(sub1, ".") == sub1
    assert r.get(sub1, "") == sub1
    assert r.get(top, "sub2") is None
    assert r.get(sub0sub0, "/top") == top
    assert r.get(sub0sub0, "/top/sub0") == sub0
    assert r.get(top, "..") is None
    assert r.get(sub0sub0, "/") is None
    assert r.get(sub0sub0, "/bar") is None


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

    assert r.glob(top, "sub0/sub0") == [sub0sub0]
    assert r.glob(sub1, "..") == [top]
    assert r.glob(sub1, "../") == [top]
    assert r.glob(sub1, "../.") == [top]
    assert r.glob(sub1, "../././.") == [top]
    assert r.glob(sub1, ".././././sub0/..") == [top]
    assert r.glob(sub1, "../sub0/sub1") == [sub0sub1]
    assert r.glob(sub1, ".") == [sub1]
    assert r.glob(sub1, "./") == [sub1]
    assert r.glob(sub1, "") == [sub1]

    assert r.glob(sub1, "/top") == [top]
    assert r.glob(sub1, "/*") == [top]

    assert r.glob(top, "*/*/sub0") == [sub0sub1sub0]
    assert r.glob(top, "sub0/sub?") == [sub0sub0, sub0sub1]
    assert r.glob(sub1, ".././*") == [sub0, sub1]
    assert r.glob(top, "*/*") == [sub0sub0, sub0sub1, sub1sub0]
    assert r.glob(top, "*/sub0") == [sub0sub0, sub1sub0]
    with assert_raises(at.RootResolverError, "Cannot go above root node Node('/top')"):
        r.glob(top, "..")
    with assert_raises(at.RootResolverError, "Cannot go above root node Node('/top')"):
        r.glob(sub1, ".././..")
    with assert_raises(at.ChildResolverError, "Node('/top/sub1') has no child sub1. Children are: 'sub0'."):
        r.glob(top, "sub1/sub1")

    with assert_raises(at.ResolverError, "unknown root node '/z*'. root is '/top'."):
        r.glob(sub1, "/z*")

    # Recursive matching
    assert r.glob(top, "**/sub0") == [sub0, sub0sub0, sub0sub1sub0, sub1sub0]
    assert r.glob(top, "**/sub0/sub0") == [sub0sub0]
    assert r.glob(top, "**/**/sub0") == [sub0, sub0sub0, sub0sub1sub0, sub1sub0]
    assert r.glob(top, "sub0/**/sub0") == [sub0sub0, sub0sub1sub0]
    with assert_raises(at.ResolverError, "unknown root node '/sub0'. root is '/top'."):
        r.glob(top, "/sub0/**/sub0")


def test_glob_relaxed():
    """Wildcard relaxed."""
    top = at.Node("top", parent=None)
    sub0 = at.Node("sub0", parent=top)
    sub0sub0 = at.Node("sub0", parent=sub0)
    sub0sub1 = at.Node("sub1", parent=sub0)
    sub0sub1sub0 = at.Node("sub0", parent=sub0sub1)
    at.Node("sub1", parent=sub0sub1)
    sub1 = at.Node("sub1", parent=top)
    sub1sub0 = at.Node("sub0", parent=sub1)
    r = at.Resolver(relax=True)

    assert r.glob(top, "sub0/sub0") == [sub0sub0]
    assert r.glob(sub1, "..") == [top]
    assert r.glob(sub1, "../") == [top]
    assert r.glob(sub1, "../.") == [top]
    assert r.glob(sub1, "../././.") == [top]
    assert r.glob(sub1, ".././././sub0/..") == [top]
    assert r.glob(sub1, "../sub0/sub1") == [sub0sub1]
    assert r.glob(sub1, ".") == [sub1]
    assert r.glob(sub1, "./") == [sub1]
    assert r.glob(sub1, "") == [sub1]

    assert r.glob(sub1, "/top") == [top]
    assert r.glob(sub1, "/*") == [top]

    assert r.glob(top, "*/*/sub0") == [sub0sub1sub0]
    assert r.glob(top, "sub0/sub?") == [sub0sub0, sub0sub1]
    assert r.glob(sub1, ".././*") == [sub0, sub1]
    assert r.glob(top, "*/*") == [sub0sub0, sub0sub1, sub1sub0]
    assert r.glob(top, "*/sub0") == [sub0sub0, sub1sub0]
    assert r.glob(top, "..") == []
    assert r.glob(sub1, ".././..") == []
    assert r.glob(top, "sub1/sub1") == []

    assert r.glob(sub1, "/z*") == []

    # Recursive matching
    assert r.glob(top, "**/sub0") == [sub0, sub0sub0, sub0sub1sub0, sub1sub0]
    assert r.glob(top, "**/sub0/sub0") == [sub0sub0]
    assert r.glob(top, "**/**/sub0") == [sub0, sub0sub0, sub0sub1sub0, sub1sub0]
    assert r.glob(top, "sub0/**/sub0") == [sub0sub0, sub0sub1sub0]
    assert r.glob(top, "/sub0/**/sub0") == []


def test_glob_cache():
    """Wildcard Cache."""
    root = at.Node("root")
    sub0 = at.Node("sub0", parent=root)
    sub1 = at.Node("sub1", parent=root)
    r = at.Resolver()
    # strip down cache size
    at.resolver._MAXCACHE = 2
    at.Resolver._match_cache.clear()
    assert len(at.Resolver._match_cache) == 0
    assert r.glob(root, "sub0") == [sub0]
    assert len(at.Resolver._match_cache) == 1
    assert r.glob(root, "sub1") == [sub1]
    assert len(at.Resolver._match_cache) == 2
    assert r.glob(root, "sub*") == [sub0, sub1]
    assert len(at.Resolver._match_cache) == 1


def test_same_name():
    """Same Name."""
    root = at.Node("root")
    sub0 = at.Node("sub", parent=root)
    sub1 = at.Node("sub", parent=root)
    r = at.Resolver()
    assert r.get(root, "sub") == sub0
    assert r.glob(root, "sub") == [sub0, sub1]


def test_ignorecase():
    """Case insensitive resolver."""
    root = at.Node("root")
    sub0 = at.Node("sUB0", parent=root)
    sub1 = at.Node("sub1", parent=root)
    r = at.Resolver(ignorecase=True)

    assert r.get(root, "SUB0") == sub0
    assert r.get(root, "sub0") == sub0
    assert r.get(root, "sUB0") == sub0
    assert r.glob(root, "SU*1") == [sub1]
    assert r.glob(root, "/*/SU*1") == [sub1]
    assert r.glob(sub0, "../*1") == [sub1]


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
    assert r.glob(root, "/ANIMAL/*") == [mammal]
    assert r.glob(root, "/ANIMAL/*/*") == [cat, dog]


def test_glob_consistency():
    """Ensure Consistency."""
    node = at.Node("root")
    resolver = at.Resolver()
    assert resolver.glob(node, "/root") == [node]
    assert resolver.get(node, "/root") == node

    assert resolver.glob(node, ".") == [node]
    assert resolver.get(node, ".") == node

    assert resolver.glob(node, "") == [node]
    assert resolver.get(node, "") == node

    with raises(at.ResolverError):
        assert resolver.glob(node, "/")
    with raises(at.ResolverError):
        assert resolver.get(node, "/")

    with raises(at.RootResolverError):
        assert resolver.glob(node, "..")
    with raises(at.RootResolverError):
        assert resolver.get(node, "..")

    with raises(at.ResolverError):
        assert resolver.glob(node, "root")
    with raises(at.ResolverError):
        assert resolver.get(node, "root")

    with raises(at.ResolverError):
        assert resolver.glob(node, "bla")
    with raises(at.ResolverError):
        assert resolver.get(node, "bla")

    with raises(at.ResolverError):
        assert resolver.glob(node, "/bla")
    with raises(at.ResolverError):
        assert resolver.get(node, "/bla")


def test_glob_consistency_relax():
    """Ensure Consistency on relaxed."""
    node = at.Node("root")
    resolver = at.Resolver(relax=True)
    assert resolver.glob(node, "/root") == [node]
    assert resolver.get(node, "/root") == node

    assert resolver.glob(node, ".") == [node]
    assert resolver.get(node, ".") == node

    assert resolver.glob(node, "") == [node]
    assert resolver.get(node, "") == node

    assert resolver.glob(node, "/") == []
    assert resolver.get(node, "/") is None

    assert resolver.glob(node, "..") == []
    assert resolver.get(node, "..") is None

    assert resolver.glob(node, "root") == []
    assert resolver.get(node, "root") is None

    assert resolver.glob(node, "bla") == []
    assert resolver.get(node, "bla") is None

    assert resolver.glob(node, "/bla") == []
    assert resolver.get(node, "/bla") is None
