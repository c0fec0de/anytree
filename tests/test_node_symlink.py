# -*- coding: utf-8 -*-
from nose.tools import eq_

from anytree import AnyNode
from anytree import Node
from anytree import NodeMixin
from anytree import PostOrderIter
from anytree import PreOrderIter
from anytree import SymlinkNode


def test_symlink():

    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root, foo=4)
    s1a = Node("sub1A", parent=s1)
    s1b = Node("sub1B", parent=s1)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)
    ln = SymlinkNode(s1, parent=root, blub=17)
    l0 = Node("l0", parent=ln)

    eq_(root.parent, None)
    eq_(root.children, tuple([s0, s1, ln]))
    eq_(s0.parent, root)
    eq_(s0.children, tuple([s0b, s0a]))
    eq_(s0b.parent, s0)
    eq_(s0b.children, tuple())
    eq_(s0a.parent, s0)
    eq_(s0a.children, tuple())
    eq_(s1.parent, root)
    eq_(s1.children, tuple([s1a, s1b, s1c]))
    eq_(s1.foo, 4)
    eq_(s1a.parent, s1)
    eq_(s1a.children, tuple())
    eq_(s1b.parent, s1)
    eq_(s1b.children, tuple())
    eq_(s1c.parent, s1)
    eq_(s1c.children, tuple([s1ca]))
    eq_(s1ca.parent, s1c)
    eq_(s1ca.children, tuple())
    eq_(ln.parent, root)
    eq_(ln.children, tuple([l0]))
    eq_(ln.foo, 4)

    eq_(s1.blub, 17)
    eq_(ln.blub, 17)

    ln.bar = 9
    eq_(ln.bar, 9)
    eq_(s1.bar, 9)

    result = [node.name for node in PreOrderIter(root)]
    eq_(result, ['root', 'sub0', 'sub0B', 'sub0A', 'sub1', 'sub1A', 'sub1B', 'sub1C', 'sub1Ca', 'sub1', 'l0'])

    result = [node.name for node in PostOrderIter(root)]
    eq_(result, ['sub0B', 'sub0A', 'sub0', 'sub1A', 'sub1B', 'sub1Ca', 'sub1C', 'sub1', 'l0', 'sub1', 'root'])
