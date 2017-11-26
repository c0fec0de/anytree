# -*- coding: utf-8 -*-

from .nodemixin import NodeMixin
from .util import _repr


class AnyNode(NodeMixin, object):

    def __init__(self, parent=None, **kwargs):
        u"""
        A generic tree node with any `kwargs`.

        >>> from anytree import AnyNode, RenderTree
        >>> root = AnyNode(id="root")
        >>> s0 = AnyNode(id="sub0", parent=root)
        >>> s0b = AnyNode(id="sub0B", parent=s0, foo=4, bar=109)
        >>> s0a = AnyNode(id="sub0A", parent=s0)
        >>> s1 = AnyNode(id="sub1", parent=root)
        >>> s1a = AnyNode(id="sub1A", parent=s1)
        >>> s1b = AnyNode(id="sub1B", parent=s1, bar=8)
        >>> s1c = AnyNode(id="sub1C", parent=s1)
        >>> s1ca = AnyNode(id="sub1Ca", parent=s1c)

        >>> root
        AnyNode(id='root')
        >>> s0
        AnyNode(id='sub0')
        >>> print(RenderTree(root))
        AnyNode(id='root')
        ├── AnyNode(id='sub0')
        │   ├── AnyNode(bar=109, foo=4, id='sub0B')
        │   └── AnyNode(id='sub0A')
        └── AnyNode(id='sub1')
            ├── AnyNode(id='sub1A')
            ├── AnyNode(bar=8, id='sub1B')
            └── AnyNode(id='sub1C')
                └── AnyNode(id='sub1Ca')
        """
        self.__dict__.update(kwargs)
        self.parent = parent

    def __repr__(self):
        return _repr(self)
