from .abstractiter import AbstractIter


class AscendingIter(AbstractIter):
    """
    Iterate upwards toward root of tree starting at `node`.

    >>> from anytree import Node, RenderTree, AsciiStyle, AscendingIter
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
    >>> [node.name for node in AscendingIter(h)]
    ['h', 'i', 'g', 'f']
    >>> [node.name for node in AscendingIter(h, maxlevel=3)]
    ['h', 'i', 'g']
    >>> [node.name for node in AscendingIter(h, filter_=lambda n: n.name not in ('e', 'g'))]
    ['h', 'i', 'f']
    >>> [node.name for node in AscendingIter(h, stop=lambda n: n.name == 'g')]
    ['h', 'i']
    """

    @staticmethod
    def _iter(children, filter_, stop, maxlevel):
        return AscendingIter.__next(children, 1, filter_, stop, maxlevel)

    @staticmethod
    def __next(children, level, filter_, stop, maxlevel):
        if not AbstractIter._abort_at_level(level, maxlevel):
            for child in children:
                if child is not None:
                    if filter_(child):
                        yield child
                    grandchildren = AbstractIter._get_children([child.parent], stop)
                    for grandchild in AscendingIter.__next(grandchildren, level + 1, filter_, stop, maxlevel):
                        yield grandchild
