
class PreOrderIter(object):

    def __init__(self, node):
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
        """
        super(PreOrderIter, self).__init__()
        self.node = node

    def __iter__(self):
        stack = tuple([self.node])
        while stack:
            node = stack[0]
            yield node
            stack = node.children + stack[1:]


class PostOrderIter(object):

    def __init__(self, node):
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
        """
        super(PostOrderIter, self).__init__()
        self.node = node

    def __iter__(self):
        return self.__next([self.node])

    @classmethod
    def __next(cls, children):
        for child in children:
            for grandchild in cls.__next(child.children):
                yield grandchild
            yield child
