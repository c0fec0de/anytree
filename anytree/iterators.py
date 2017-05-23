# -*- coding: utf-8 -*-
"""
Tree Iteration.

* :any:`PreOrderIter`: iterate over tree using pre-order strategy (self, children)
* :any:`PostOrderIter`: iterate over tree using post-order strategy (children, self)
* :any:`LevelOrderIter`: iterate over tree using level-order strategy
* :any:`LevelOrderGroupIter`: iterate over tree using level-order strategy returning group for every level
* :any:`ZigZagGroupIter`: iterate over tree using level-order strategy returning group for every level
"""
import six


class AbstractIter(six.Iterator):

    def __init__(self, node, filter_=None, stop=None, maxlevel=None):
        """
        Base class for all iterators.

        Iterate over tree starting at `node`.

        Keyword Args:
            filter_: function called with every `node` as argument, `node` is returned if `True`.
            stop: stop iteration at `node` if `stop` function returns `True` for `node`.
            maxlevel (int): maximum decending in the node hierarchy.
        """
        self.node = node
        self.filter_ = filter_
        self.stop = stop
        self.maxlevel = maxlevel
        self.__iter = None

    def __init(self):
        node = self.node
        filter_ = self.filter_
        stop = self.stop
        maxlevel = self.maxlevel
        if filter_ is None:
            def filter_(node):
                return True
        if stop is None:
            def stop(node):
                return False
        children = [] if AbstractIter._abort_at_level(1, maxlevel) else AbstractIter._get_children([node], stop)
        return self._iter(children, filter_, stop, maxlevel)

    def __iter__(self):
        return self.__init()

    def __next__(self):
        if self.__iter is None:
            self.__iter = self.__init()
        return next(self.__iter)

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        raise NotImplementedError()  # pragma: no cover

    @staticmethod
    def _abort_at_level(level, maxlevel):
        return maxlevel is not None and level > maxlevel

    @staticmethod
    def _get_children(children, stop):
        return [child for child in children if not stop(child)]


class PreOrderIter(AbstractIter):

    """
    Iterate over tree applying pre-order strategy starting at `node`.

    Start at root and go-down until reaching a leaf node.
    Step upwards then, and search for the next leafs.

    >>> from anytree import Node, RenderTree, AsciiStyle
    >>> f = Node("f")
    >>> b = Node("b", parent=f)
    >>> a = Node("a", parent=b)
    >>> d = Node("d", parent=b)
    >>> c = Node("c", parent=d)
    >>> e = Node("e", parent=d)
    >>> g = Node("g", parent=f)
    >>> i = Node("i", parent=g)
    >>> h = Node("h", parent=i)
    >>> print(RenderTree(f, style=AsciiStyle()).by_attr())
    f
    |-- b
    |   |-- a
    |   +-- d
    |       |-- c
    |       +-- e
    +-- g
        +-- i
            +-- h
    >>> [node.name for node in PreOrderIter(f)]
    ['f', 'b', 'a', 'd', 'c', 'e', 'g', 'i', 'h']
    >>> [node.name for node in PreOrderIter(f, maxlevel=3)]
    ['f', 'b', 'a', 'd', 'g', 'i']
    >>> [node.name for node in PreOrderIter(f, filter_=lambda n: n.name not in ('e', 'g'))]
    ['f', 'b', 'a', 'd', 'c', 'i', 'h']
    >>> [node.name for node in PreOrderIter(f, stop=lambda n: n.name == 'd')]
    ['f', 'b', 'a', 'g', 'i', 'h']
    """

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        stack = [children]
        while stack:
            children = stack[-1]
            if children:
                child = children.pop(0)
                if filter_(child):
                    yield child
                if not AbstractIter._abort_at_level(len(stack) + 1, maxlevel):
                    grandchildren = AbstractIter._get_children(child.children, stop)
                    if grandchildren:
                        stack.append(grandchildren)
            else:
                stack.pop()


class PostOrderIter(AbstractIter):

    """
    Iterate over tree applying post-order strategy starting at `node`.

    >>> from anytree import Node, RenderTree, AsciiStyle
    >>> f = Node("f")
    >>> b = Node("b", parent=f)
    >>> a = Node("a", parent=b)
    >>> d = Node("d", parent=b)
    >>> c = Node("c", parent=d)
    >>> e = Node("e", parent=d)
    >>> g = Node("g", parent=f)
    >>> i = Node("i", parent=g)
    >>> h = Node("h", parent=i)
    >>> print(RenderTree(f, style=AsciiStyle()).by_attr())
    f
    |-- b
    |   |-- a
    |   +-- d
    |       |-- c
    |       +-- e
    +-- g
        +-- i
            +-- h
    >>> [node.name for node in PostOrderIter(f)]
    ['a', 'c', 'e', 'd', 'b', 'h', 'i', 'g', 'f']
    >>> [node.name for node in PostOrderIter(f, maxlevel=3)]
    ['a', 'd', 'b', 'i', 'g', 'f']
    >>> [node.name for node in PostOrderIter(f, filter_=lambda n: n.name not in ('e', 'g'))]
    ['a', 'c', 'd', 'b', 'h', 'i', 'f']
    >>> [node.name for node in PostOrderIter(f, stop=lambda n: n.name == 'd')]
    ['a', 'b', 'h', 'i', 'g', 'f']
    """

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        return PostOrderIter.__next(children, 1, filter_, stop, maxlevel)

    @staticmethod
    def __next(children, level, filter_, stop, maxlevel):
        if not AbstractIter._abort_at_level(level, maxlevel):
            for child in children:
                grandchildren = AbstractIter._get_children(child.children, stop)
                for grandchild in PostOrderIter.__next(grandchildren, level + 1, filter_, stop, maxlevel):
                    yield grandchild
                if filter_(child):
                    yield child


class LevelOrderIter(AbstractIter):

    """
    Iterate over tree applying level-order strategy starting at `node`.

    >>> from anytree import Node, RenderTree, AsciiStyle
    >>> f = Node("f")
    >>> b = Node("b", parent=f)
    >>> a = Node("a", parent=b)
    >>> d = Node("d", parent=b)
    >>> c = Node("c", parent=d)
    >>> e = Node("e", parent=d)
    >>> g = Node("g", parent=f)
    >>> i = Node("i", parent=g)
    >>> h = Node("h", parent=i)
    >>> print(RenderTree(f, style=AsciiStyle()).by_attr())
    f
    |-- b
    |   |-- a
    |   +-- d
    |       |-- c
    |       +-- e
    +-- g
        +-- i
            +-- h
    >>> [node.name for node in LevelOrderIter(f)]
    ['f', 'b', 'g', 'a', 'd', 'i', 'c', 'e', 'h']
    >>> [node.name for node in LevelOrderIter(f, maxlevel=3)]
    ['f', 'b', 'g', 'a', 'd', 'i']
    >>> [node.name for node in LevelOrderIter(f, filter_=lambda n: n.name not in ('e', 'g'))]
    ['f', 'b', 'a', 'd', 'i', 'c', 'h']
    >>> [node.name for node in LevelOrderIter(f, stop=lambda n: n.name == 'd')]
    ['f', 'b', 'g', 'a', 'i', 'h']
    """

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        level = 1
        while children:
            next_children = []
            for child in children:
                if filter_(child):
                    yield child
                next_children += AbstractIter._get_children(child.children, stop)
            children = next_children
            level += 1
            if AbstractIter._abort_at_level(level, maxlevel):
                break


class LevelOrderGroupIter(AbstractIter):

    """
    Iterate over tree applying level-order strategy with grouping starting at `node`.

    Return a tuple of nodes for each level. The first tuple contains the
    nodes at level 0 (always `node`). The second tuple contains the nodes at level 1
    (children of `node`). The next level contains the children of the children, and so on.

    >>> from anytree import Node, RenderTree, AsciiStyle
    >>> f = Node("f")
    >>> b = Node("b", parent=f)
    >>> a = Node("a", parent=b)
    >>> d = Node("d", parent=b)
    >>> c = Node("c", parent=d)
    >>> e = Node("e", parent=d)
    >>> g = Node("g", parent=f)
    >>> i = Node("i", parent=g)
    >>> h = Node("h", parent=i)
    >>> print(RenderTree(f, style=AsciiStyle()).by_attr())
    f
    |-- b
    |   |-- a
    |   +-- d
    |       |-- c
    |       +-- e
    +-- g
        +-- i
            +-- h
    >>> [[node.name for node in children] for children in LevelOrderGroupIter(f)]
    [['f'], ['b', 'g'], ['a', 'd', 'i'], ['c', 'e', 'h']]
    >>> [[node.name for node in children] for children in LevelOrderGroupIter(f, maxlevel=3)]
    [['f'], ['b', 'g'], ['a', 'd', 'i']]
    >>> [[node.name for node in children]
    ...  for children in LevelOrderGroupIter(f, filter_=lambda n: n.name not in ('e', 'g'))]
    [['f'], ['b'], ['a', 'd', 'i'], ['c', 'h']]
    >>> [[node.name for node in children]
    ...  for children in LevelOrderGroupIter(f, stop=lambda n: n.name == 'd')]
    [['f'], ['b', 'g'], ['a', 'i'], ['h']]
    """

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        level = 1
        while children:
            yield tuple([child for child in children if filter_(child)])
            level += 1
            if AbstractIter._abort_at_level(level, maxlevel):
                break
            children = LevelOrderGroupIter._get_grandchildren(children, stop)

    @staticmethod
    def _get_grandchildren(children, stop):
        next_children = []
        for child in children:
            next_children = next_children + AbstractIter._get_children(child.children, stop)
        return next_children


class ZigZagGroupIter(AbstractIter):

    """
    Iterate over tree applying Zig-Zag strategy with grouping starting at `node`.

    Return a tuple of nodes for each level. The first tuple contains the
    nodes at level 0 (always `node`). The second tuple contains the nodes at level 1
    (children of `node`) in reversed order.
    The next level contains the children of the children in forward order, and so on.

    >>> from anytree import Node, RenderTree, AsciiStyle
    >>> f = Node("f")
    >>> b = Node("b", parent=f)
    >>> a = Node("a", parent=b)
    >>> d = Node("d", parent=b)
    >>> c = Node("c", parent=d)
    >>> e = Node("e", parent=d)
    >>> g = Node("g", parent=f)
    >>> i = Node("i", parent=g)
    >>> h = Node("h", parent=i)
    >>> print(RenderTree(f, style=AsciiStyle()).by_attr())
    f
    |-- b
    |   |-- a
    |   +-- d
    |       |-- c
    |       +-- e
    +-- g
        +-- i
            +-- h
    >>> [[node.name for node in children] for children in ZigZagGroupIter(f)]
    [['f'], ['g', 'b'], ['a', 'd', 'i'], ['h', 'e', 'c']]
    >>> [[node.name for node in children] for children in ZigZagGroupIter(f, maxlevel=3)]
    [['f'], ['g', 'b'], ['a', 'd', 'i']]
    >>> [[node.name for node in children]
    ...  for children in ZigZagGroupIter(f, filter_=lambda n: n.name not in ('e', 'g'))]
    [['f'], ['b'], ['a', 'd', 'i'], ['h', 'c']]
    >>> [[node.name for node in children]
    ...  for children in ZigZagGroupIter(f, stop=lambda n: n.name == 'd')]
    [['f'], ['g', 'b'], ['a', 'i'], ['h']]
    """

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        _iter = LevelOrderGroupIter._iter(children, filter_, stop, maxlevel)
        while True:
            yield next(_iter)
            yield tuple(reversed(next(_iter)))
