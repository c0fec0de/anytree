# -*- coding: utf-8 -*-
"""
Tree Iteration.

* :any:`PreOrderIter`: iterate over tree using pre-order strategy
* :any:`PostOrderIter`: iterate over tree using post-order strategy
* :any:`LevelOrderIter`: iterate over tree using level-order strategy
* :any:`LevelGroupOrderIter`: iterate over tree using level-order strategy returning group for every level
"""


class AbstractIter(object):

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

    def __iter__(self):
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
        children = [node] if (maxlevel is None) or (maxlevel > 0) and not stop(node) else []
        return self._iter(children, filter_, stop, maxlevel)

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        raise NotImplementedError()  # pragma: no cover


class PreOrderIter(AbstractIter):

    def __init__(self, node, filter_=None, stop=None, maxlevel=None):
        """
        Iterate over tree applying pre-order strategy starting at `node`.

        Start at root and go-down until reaching a leaf node.
        Step upwards then, and search for the next leafs.

        Keyword Args:
            filter_: function called with every `node` as argument, `node` is returned if `True`.
            stop: stop iteration at `node` if `stop` function returns `True` for `node`.
            maxlevel (int): maximum decending in the node hierarchy.

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
        >>> print(RenderTree(f, style=AsciiStyle()))
        Node('/f')
        |-- Node('/f/b')
        |   |-- Node('/f/b/a')
        |   +-- Node('/f/b/d')
        |       |-- Node('/f/b/d/c')
        |       +-- Node('/f/b/d/e')
        +-- Node('/f/g')
            +-- Node('/f/g/i')
                +-- Node('/f/g/i/h')
        >>> [node.name for node in PreOrderIter(f)]
        ['f', 'b', 'a', 'd', 'c', 'e', 'g', 'i', 'h']
        >>> [node.name for node in PreOrderIter(f, maxlevel=0)]
        []
        >>> [node.name for node in PreOrderIter(f, maxlevel=3)]
        ['f', 'b', 'a', 'd', 'g', 'i']
        >>> [node.name for node in PreOrderIter(f, filter_=lambda n: n.name not in ('e', 'g'))]
        ['f', 'b', 'a', 'd', 'c', 'i', 'h']
        >>> [node.name for node in PreOrderIter(f, stop=lambda n: n.name == 'd')]
        ['f', 'b', 'a', 'g', 'i', 'h']
        """
        super(PreOrderIter, self).__init__(node, filter_=filter_, stop=stop, maxlevel=maxlevel)

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        stack = [children]
        while stack:
            children = stack[-1]
            if children:
                child = children.pop(0)
                if not stop(child):
                    if filter_(child):
                        yield child
                    grandchildren = list(child.children)
                    if grandchildren and (maxlevel is None or len(stack) < maxlevel):
                        stack.append(grandchildren)
            else:
                stack.pop()


class PostOrderIter(AbstractIter):

    def __init__(self, node, filter_=None, stop=None, maxlevel=None):
        """
        Iterate over tree applying post-order strategy starting at `node`.

        Keyword Args:
            filter_: function called with every `node` as argument, `node` is returned if `True`.
            stop: stop iteration at `node` if `stop` function returns `True` for `node`.
            maxlevel (int): maximum decending in the node hierarchy.

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
        >>> print(RenderTree(f, style=AsciiStyle()))
        Node('/f')
        |-- Node('/f/b')
        |   |-- Node('/f/b/a')
        |   +-- Node('/f/b/d')
        |       |-- Node('/f/b/d/c')
        |       +-- Node('/f/b/d/e')
        +-- Node('/f/g')
            +-- Node('/f/g/i')
                +-- Node('/f/g/i/h')
        >>> [node.name for node in PostOrderIter(f)]
        ['a', 'c', 'e', 'd', 'b', 'h', 'i', 'g', 'f']
        >>> [node.name for node in PostOrderIter(f, maxlevel=0)]
        []
        >>> [node.name for node in PostOrderIter(f, maxlevel=3)]
        ['a', 'd', 'b', 'i', 'g', 'f']
        >>> [node.name for node in PostOrderIter(f, filter_=lambda n: n.name not in ('e', 'g'))]
        ['a', 'c', 'd', 'b', 'h', 'i', 'f']
        >>> [node.name for node in PostOrderIter(f, stop=lambda n: n.name == 'd')]
        ['a', 'b', 'h', 'i', 'g', 'f']
        """
        super(PostOrderIter, self).__init__(node, filter_=filter_, stop=stop, maxlevel=maxlevel)

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        return PostOrderIter.__next(children, 1, filter_, stop, maxlevel)

    @staticmethod
    def __next(children, level, filter_, stop, maxlevel):
        if maxlevel is None or level <= maxlevel:
            for child in children:
                if not stop(child):
                    for grandchild in PostOrderIter.__next(child.children, level + 1, filter_, stop, maxlevel):
                        yield grandchild
                    if filter_(child):
                        yield child


class LevelOrderIter(AbstractIter):

    def __init__(self, node, filter_=None, stop=None, maxlevel=None):
        """
        Iterate over tree applying level-order strategy starting at `node`.

        Keyword Args:
            filter_: function called with every `node` as argument, `node` is returned if `True`.
            stop: stop iteration at `node` if `stop` function returns `True` for `node`.
            maxlevel (int): maximum decending in the node hierarchy.

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
        >>> print(RenderTree(f, style=AsciiStyle()))
        Node('/f')
        |-- Node('/f/b')
        |   |-- Node('/f/b/a')
        |   +-- Node('/f/b/d')
        |       |-- Node('/f/b/d/c')
        |       +-- Node('/f/b/d/e')
        +-- Node('/f/g')
            +-- Node('/f/g/i')
                +-- Node('/f/g/i/h')
        >>> [node.name for node in LevelOrderIter(f)]
        ['f', 'b', 'g', 'a', 'd', 'i', 'c', 'e', 'h']
        >>> [node.name for node in LevelOrderIter(f, maxlevel=0)]
        []
        >>> [node.name for node in LevelOrderIter(f, maxlevel=3)]
        ['f', 'b', 'g', 'a', 'd', 'i']
        >>> [node.name for node in LevelOrderIter(f, filter_=lambda n: n.name not in ('e', 'g'))]
        ['f', 'b', 'a', 'd', 'i', 'c', 'h']
        >>> [node.name for node in LevelOrderIter(f, stop=lambda n: n.name == 'd')]
        ['f', 'b', 'g', 'a', 'i', 'h']
        """
        super(LevelOrderIter, self).__init__(node, filter_=filter_, stop=stop, maxlevel=maxlevel)

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        level = 1
        while children:
            next_children = []
            for child in children:
                if not stop(child):
                    if filter_(child):
                        yield child
                    next_children += child.children
            children = next_children
            level += 1
            if maxlevel is not None and level > maxlevel:
                break


class LevelGroupOrderIter(AbstractIter):

    def __init__(self, node, filter_=None, stop=None, maxlevel=None):
        """
        Iterate over tree applying level-order strategy with grouping starting at `node`.

        Return a tuple of nodes for each level. The first tuple contains the
        nodes at level 0 (always `node`). The second tuple contains the nodes at level 1
        (children of `node`). The next level contains the children of the children, and so on.

        Keyword Args:
            filter_: function called with every `node` as argument, `node` is returned if `True`.
            stop: stop iteration at `node` if `stop` function returns `True` for `node`.
            maxlevel (int): maximum decending in the node hierarchy.

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
        >>> print(RenderTree(f, style=AsciiStyle()))
        Node('/f')
        |-- Node('/f/b')
        |   |-- Node('/f/b/a')
        |   +-- Node('/f/b/d')
        |       |-- Node('/f/b/d/c')
        |       +-- Node('/f/b/d/e')
        +-- Node('/f/g')
            +-- Node('/f/g/i')
                +-- Node('/f/g/i/h')
        >>> [[node.name for node in children] for children in LevelGroupOrderIter(f)]
        [['f'], ['b', 'g'], ['a', 'd', 'i'], ['c', 'e', 'h']]
        >>> [[node.name for node in children] for children in LevelGroupOrderIter(f, maxlevel=0)]
        []
        >>> [[node.name for node in children] for children in LevelGroupOrderIter(f, maxlevel=3)]
        [['f'], ['b', 'g'], ['a', 'd', 'i']]
        >>> [[node.name for node in children]
        ...  for children in LevelGroupOrderIter(f, filter_=lambda n: n.name not in ('e', 'g'))]
        [['f'], ['b'], ['a', 'd', 'i'], ['c', 'h']]
        >>> [[node.name for node in children]
        ...  for children in LevelGroupOrderIter(f, stop=lambda n: n.name == 'd')]
        [['f'], ['b', 'g'], ['a', 'i'], ['h']]
        """
        super(LevelGroupOrderIter, self).__init__(node, filter_=filter_, stop=stop, maxlevel=maxlevel)

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        level = 1
        while children:
            yield tuple([child for child in children if filter_(child)])
            level += 1
            if maxlevel is not None and level > maxlevel:
                break
            children = LevelGroupOrderIter._get_children(children, stop)

    @staticmethod
    def _get_children(children, stop):
            next_children = []
            for child in children:
                next_children = next_children + [c for c in child.children if not stop(c)]
            return next_children
