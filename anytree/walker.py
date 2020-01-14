# -*- coding: utf-8 -*-


class Walker(object):

    def __init__(self):
        """Walk from one node to another."""
        super(Walker, self).__init__()

    def walk(self, start, end):
        """
        Walk from `start` node to `end` node.

        Returns:
            (upwards, common, downwards): `upwards` is a list of nodes to go upward to.
            `common` top node. `downwards` is a list of nodes to go downward to.

        Raises:
            WalkError: on no common root node.

        Example:

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

        Create a walker:

        >>> w = Walker()

        This class is made for walking:

        >>> w.walk(f, f)
        ((), Node('/f'), ())
        >>> w.walk(f, b)
        ((), Node('/f'), (Node('/f/b'),))
        >>> w.walk(b, f)
        ((Node('/f/b'),), Node('/f'), ())
        >>> w.walk(h, e)
        ((Node('/f/g/i/h'), Node('/f/g/i'), Node('/f/g')), Node('/f'), (Node('/f/b'), Node('/f/b/d'), Node('/f/b/d/e')))
        >>> w.walk(d, e)
        ((), Node('/f/b/d'), (Node('/f/b/d/e'),))

        For a proper walking the nodes need to be part of the same tree:

        >>> w.walk(Node("a"), Node("b"))
        Traceback (most recent call last):
          ...
        anytree.walker.WalkError: Node('/a') and Node('/b') are not part of the same tree.
        """
        s = start.path
        e = end.path
        if start.root is not end.root:
            msg = "%r and %r are not part of the same tree." % (start, end)
            raise WalkError(msg)
        # common
        c = Walker.__calc_common(s, e)
        assert c[0] is start.root
        len_c = len(c)
        # up
        if start is c[-1]:
            up = tuple()
        else:
            up = tuple(reversed(s[len_c:]))
        # down
        if end is c[-1]:
            down = tuple()
        else:
            down = e[len_c:]
        return up, c[-1], down

    @staticmethod
    def __calc_common(s, e):
        return tuple([si for si, ei in zip(s, e) if si is ei])


class WalkError(RuntimeError):
    """Walk Error."""
