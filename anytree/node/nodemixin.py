# -*- coding: utf-8 -*-

import warnings

from anytree.iterators import PreOrderIter

from .exceptions import LoopError
from .exceptions import TreeError


class NodeMixin(object):

    separator = "/"

    u"""
    The :any:`NodeMixin` class extends any Python class to a tree node.

    The only tree relevant information is the `parent` attribute.
    If `None` the :any:`NodeMixin` is root node.
    If set to another node, the :any:`NodeMixin` becomes the child of it.

    >>> from anytree import NodeMixin, RenderTree
    >>> class MyBaseClass(object):
    ...     foo = 4
    >>> class MyClass(MyBaseClass, NodeMixin):  # Add Node feature
    ...     def __init__(self, name, length, width, parent=None):
    ...         super(MyClass, self).__init__()
    ...         self.name = name
    ...         self.length = length
    ...         self.width = width
    ...         self.parent = parent

    >>> my0 = MyClass('my0', 0, 0)
    >>> my1 = MyClass('my1', 1, 0, parent=my0)
    >>> my2 = MyClass('my2', 0, 2, parent=my0)

    >>> for pre, _, node in RenderTree(my0):
    ...     treestr = u"%s%s" % (pre, node.name)
    ...     print(treestr.ljust(8), node.length, node.width)
    my0      0 0
    ├── my1  1 0
    └── my2  0 2
    """

    @property
    def parent(self):
        u"""
        Parent Node.

        On set, the node is detached from any previous parent node and attached
        to the new node.

        >>> from anytree import Node, RenderTree
        >>> udo = Node("Udo")
        >>> marc = Node("Marc")
        >>> lian = Node("Lian", parent=marc)
        >>> print(RenderTree(udo))
        Node('/Udo')
        >>> print(RenderTree(marc))
        Node('/Marc')
        └── Node('/Marc/Lian')

        **Attach**

        >>> marc.parent = udo
        >>> print(RenderTree(udo))
        Node('/Udo')
        └── Node('/Udo/Marc')
            └── Node('/Udo/Marc/Lian')

        **Detach**

        To make a node to a root node, just set this attribute to `None`.

        >>> marc.is_root
        False
        >>> marc.parent = None
        >>> marc.is_root
        True
        """
        try:
            return self.__parent
        except AttributeError:
            return None

    @parent.setter
    def parent(self, value):
        if value is not None and not isinstance(value, NodeMixin):
            msg = "Parent node %r is not of type 'NodeMixin'." % (value)
            raise TreeError(msg)
        try:
            parent = self.__parent
        except AttributeError:
            parent = None
        if parent is not value:
            self.__check_loop(value)
            self.__detach(parent)
            self.__attach(value)

    def __check_loop(self, node):
        if node is not None:
            if node is self:
                msg = "Cannot set parent. %r cannot be parent of itself."
                raise LoopError(msg % self)
            if self in node.path:
                msg = "Cannot set parent. %r is parent of %r."
                raise LoopError(msg % (self, node))

    def __detach(self, parent):
        if parent is not None:
            self._pre_detach(parent)
            parentchildren = parent.__children_
            assert self in parentchildren, "Tree internal data is corrupt."
            # ATOMIC START
            parentchildren.remove(self)
            self.__parent = None
            # ATOMIC END
            self._post_detach(parent)

    def __attach(self, parent):
        if parent is not None:
            self._pre_attach(parent)
            parentchildren = parent.__children_
            assert self not in parentchildren, "Tree internal data is corrupt."
            # ATOMIC START
            parentchildren.append(self)
            self.__parent = parent
            # ATOMIC END
            self._post_attach(parent)

    @property
    def __children_(self):
        try:
            return self.__children
        except AttributeError:
            self.__children = []
            return self.__children

    @property
    def children(self):
        """
        All child nodes.

        >>> from anytree import Node
        >>> n = Node("n")
        >>> a = Node("a", parent=n)
        >>> b = Node("b", parent=n)
        >>> c = Node("c", parent=n)
        >>> n.children
        (Node('/n/a'), Node('/n/b'), Node('/n/c'))

        Modifying the children attribute modifies the tree.

        **Detach**

        The children attribute can be updated by setting to an iterable.

        >>> n.children = [a, b]
        >>> n.children
        (Node('/n/a'), Node('/n/b'))

        Node `c` is removed from the tree.
        In case of an existing reference, the node `c` does not vanish and is the root of its own tree.

        >>> c
        Node('/c')

        **Attach**

        >>> d = Node("d")
        >>> d
        Node('/d')
        >>> n.children = [a, b, d]
        >>> n.children
        (Node('/n/a'), Node('/n/b'), Node('/n/d'))
        >>> d
        Node('/n/d')

        **Duplicate**

        A node can just be the children once. Duplicates cause a :any:`TreeError`:

        >>> n.children = [a, b, d, a]
        Traceback (most recent call last):
            ...
        anytree.node.exceptions.TreeError: Cannot add node Node('/n/a') multiple times as child.
        """
        return tuple(self.__children_)

    @staticmethod
    def __check_children(children):
        seen = set()
        for child in children:
            if not isinstance(child, NodeMixin):
                msg = ("Cannot add non-node object %r. "
                       "It is not a subclass of 'NodeMixin'.") % child
                raise TreeError(msg)
            if child not in seen:
                seen.add(child)
            else:
                msg = "Cannot add node %r multiple times as child." % child
                raise TreeError(msg)

    @children.setter
    def children(self, children):
        # convert iterable to tuple
        children = tuple(children)
        NodeMixin.__check_children(children)
        # ATOMIC start
        old_children = self.children
        del self.children
        try:
            self._pre_attach_children(children)
            for child in children:
                child.parent = self
            self._post_attach_children(children)
            assert len(self.children) == len(children)
        except Exception:
            self.children = old_children
            raise
        # ATOMIC end

    @children.deleter
    def children(self):
        children = self.children
        self._pre_detach_children(children)
        for child in self.children:
            child.parent = None
        assert len(self.children) == 0
        self._post_detach_children(children)

    def _pre_detach_children(self, children):
        """Method call before detaching `children`."""
        pass

    def _post_detach_children(self, children):
        """Method call after detaching `children`."""
        pass

    def _pre_attach_children(self, children):
        """Method call before attaching `children`."""
        pass

    def _post_attach_children(self, children):
        """Method call after attaching `children`."""
        pass

    @property
    def path(self):
        """
        Path of this `Node`.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> udo.path
        (Node('/Udo'),)
        >>> marc.path
        (Node('/Udo'), Node('/Udo/Marc'))
        >>> lian.path
        (Node('/Udo'), Node('/Udo/Marc'), Node('/Udo/Marc/Lian'))
        """
        return self._path

    @property
    def _path(self):
        path = []
        node = self
        while node:
            path.insert(0, node)
            node = node.parent
        return tuple(path)

    @property
    def ancestors(self):
        """
        All parent nodes and their parent nodes.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> udo.ancestors
        ()
        >>> marc.ancestors
        (Node('/Udo'),)
        >>> lian.ancestors
        (Node('/Udo'), Node('/Udo/Marc'))
        """
        return self._path[:-1]

    @property
    def anchestors(self):
        """
        All parent nodes and their parent nodes - see :any:`ancestors`.

        The attribute `anchestors` is just a typo of `ancestors`. Please use `ancestors`.
        This attribute will be removed in the 2.0.0 release.
        """
        warnings.warn(".anchestors was a typo and will be removed in version 3.0.0", DeprecationWarning)
        return self.ancestors

    @property
    def descendants(self):
        """
        All child nodes and all their child nodes.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> loui = Node("Loui", parent=marc)
        >>> soe = Node("Soe", parent=lian)
        >>> udo.descendants
        (Node('/Udo/Marc'), Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Lian/Soe'), Node('/Udo/Marc/Loui'))
        >>> marc.descendants
        (Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Lian/Soe'), Node('/Udo/Marc/Loui'))
        >>> lian.descendants
        (Node('/Udo/Marc/Lian/Soe'),)
        """
        return tuple(PreOrderIter(self))[1:]

    @property
    def root(self):
        """
        Tree Root Node.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> udo.root
        Node('/Udo')
        >>> marc.root
        Node('/Udo')
        >>> lian.root
        Node('/Udo')
        """
        if self.parent:
            return self._path[0]
        else:
            return self

    @property
    def siblings(self):
        """
        Tuple of nodes with the same parent.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> loui = Node("Loui", parent=marc)
        >>> lazy = Node("Lazy", parent=marc)
        >>> udo.siblings
        ()
        >>> marc.siblings
        ()
        >>> lian.siblings
        (Node('/Udo/Marc/Loui'), Node('/Udo/Marc/Lazy'))
        >>> loui.siblings
        (Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Lazy'))
        """
        parent = self.parent
        if parent is None:
            return tuple()
        else:
            return tuple([node for node in parent.children if node != self])

    @property
    def is_leaf(self):
        """
        `Node` has no children (External Node).

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> udo.is_leaf
        False
        >>> marc.is_leaf
        False
        >>> lian.is_leaf
        True
        """
        return len(self.__children_) == 0

    @property
    def is_root(self):
        """
        `Node` is tree root.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> udo.is_root
        True
        >>> marc.is_root
        False
        >>> lian.is_root
        False
        """
        return self.parent is None

    @property
    def height(self):
        """
        Number of edges on the longest path to a leaf `Node`.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> udo.height
        2
        >>> marc.height
        1
        >>> lian.height
        0
        """
        if self.__children_:
            return max([child.height for child in self.__children_]) + 1
        else:
            return 0

    @property
    def depth(self):
        """
        Number of edges to the root `Node`.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> udo.depth
        0
        >>> marc.depth
        1
        >>> lian.depth
        2
        """
        return len(self._path) - 1

    def _pre_detach(self, parent):
        """Method call before detaching from `parent`."""
        pass

    def _post_detach(self, parent):
        """Method call after detaching from `parent`."""
        pass

    def _pre_attach(self, parent):
        """Method call before attaching to `parent`."""
        pass

    def _post_attach(self, parent):
        """Method call after attaching to `parent`."""
        pass
