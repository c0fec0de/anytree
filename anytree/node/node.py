# -*- coding: utf-8 -*-

from .nodemixin import NodeMixin
from .util import _repr


class Node(NodeMixin, object):

    def __init__(self, name, parent=None, **kwargs):
        u"""
        A simple tree node with a `name` and any `kwargs`.

        >>> from anytree import Node, RenderTree
        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root)
        >>> s0b = Node("sub0B", parent=s0, foo=4, bar=109)
        >>> s0a = Node("sub0A", parent=s0)
        >>> s1 = Node("sub1", parent=root)
        >>> s1a = Node("sub1A", parent=s1)
        >>> s1b = Node("sub1B", parent=s1, bar=8)
        >>> s1c = Node("sub1C", parent=s1)
        >>> s1ca = Node("sub1Ca", parent=s1c)

        >>> print(RenderTree(root))
        Node('/root')
        ├── Node('/root/sub0')
        │   ├── Node('/root/sub0/sub0B', bar=109, foo=4)
        │   └── Node('/root/sub0/sub0A')
        └── Node('/root/sub1')
            ├── Node('/root/sub1/sub1A')
            ├── Node('/root/sub1/sub1B', bar=8)
            └── Node('/root/sub1/sub1C')
                └── Node('/root/sub1/sub1C/sub1Ca')
        """
        self.__dict__.update(kwargs)
        self.name = name
        self.parent = parent

    def __repr__(self):
        args = ["%r" % self.separator.join([""] + [str(node.name) for node in self.path])]
        return _repr(self, args=args, nameblacklist=["name"])
