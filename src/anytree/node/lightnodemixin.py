from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar, Union, cast

from anytree.config import ASSERTIONS
from anytree.iterators import PreOrderIter

from .exceptions import LoopError, TreeError

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

    from typing_extensions import Any

    from .nodemixin import NodeMixin

NodeT_co = TypeVar("NodeT_co", bound=Union["NodeMixin[Any]", "LightNodeMixin[Any]"], covariant=True)


class LightNodeMixin(Generic[NodeT_co]):
    """
    The :any:`LightNodeMixin` behaves identical to :any:`NodeMixin`, but uses `__slots__`.

    There are some minor differences in the object behaviour.
    See slots_ for any details.

    .. _slots: https://docs.python.org/3/reference/datamodel.html#slots

    The only tree relevant information is the `parent` attribute.
    If `None` the :any:`LightNodeMixin` is root node.
    If set to another node, the :any:`LightNodeMixin` becomes the child of it.

    The `children` attribute can be used likewise.
    If `None` the :any:`LightNodeMixin` has no children.
    The `children` attribute can be set to any iterable of :any:`LightNodeMixin` instances.
    These instances become children of the node.

    >>> from anytree import LightNodeMixin, RenderTree
    >>> class MyBaseClass():  # Just an example of a base class
    ...     __slots__ = []
    >>> class MyClass(MyBaseClass, LightNodeMixin):  # Add Node feature
    ...     __slots__ = ['name', 'length', 'width']
    ...     def __init__(self, name, length, width, parent=None, children=None):
    ...         super().__init__()
    ...         self.name = name
    ...         self.length = length
    ...         self.width = width
    ...         self.parent = parent
    ...         if children:
    ...             self.children = children

    Construction via `parent`:

    >>> my0 = MyClass('my0', 0, 0)
    >>> my1 = MyClass('my1', 1, 0, parent=my0)
    >>> my2 = MyClass('my2', 0, 2, parent=my0)

    >>> for pre, _, node in RenderTree(my0):
    ...     treestr = u"%s%s" % (pre, node.name)
    ...     print(treestr.ljust(8), node.length, node.width)
    my0      0 0
    ├── my1  1 0
    └── my2  0 2

    Construction via `children`:

    >>> my0 = MyClass('my0', 0, 0, children=[
    ...     MyClass('my1', 1, 0),
    ...     MyClass('my2', 0, 2),
    ... ])

    >>> for pre, _, node in RenderTree(my0):
    ...     treestr = u"%s%s" % (pre, node.name)
    ...     print(treestr.ljust(8), node.length, node.width)
    my0      0 0
    ├── my1  1 0
    └── my2  0 2

    Both approaches can be mixed:

    >>> my0 = MyClass('my0', 0, 0, children=[
    ...     MyClass('my1', 1, 0),
    ... ])
    >>> my2 = MyClass('my2', 0, 2, parent=my0)

    >>> for pre, _, node in RenderTree(my0):
    ...     treestr = u"%s%s" % (pre, node.name)
    ...     print(treestr.ljust(8), node.length, node.width)
    my0      0 0
    ├── my1  1 0
    └── my2  0 2
    """

    __slots__ = ["__children", "__parent"]

    separator = "/"

    @property
    def parent(self) -> NodeT_co | None:
        """
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
        if hasattr(self, "_LightNodeMixin__parent"):
            return self.__parent
        return None

    @parent.setter
    def parent(self, value: NodeT_co | None) -> None:
        if hasattr(self, "_LightNodeMixin__parent"):
            parent = self.__parent
        else:
            parent = None
        if parent is not value:
            self.__check_loop(value)
            self.__detach(parent)
            self.__attach(value)

    def __check_loop(self, node: NodeT_co | None) -> None:
        if node is not None:
            if node is self:
                msg = "Cannot set parent. %r cannot be parent of itself."
                raise LoopError(msg % (self,))
            if any(child is self for child in node.iter_path_reverse()):
                msg = "Cannot set parent. %r is parent of %r."
                raise LoopError(msg % (self, node))

    def __detach(self, parent: NodeT_co | None) -> None:
        # pylint: disable=W0212,W0238
        if parent is not None:
            self._pre_detach(parent)
            parentchildren = parent.__children_or_empty
            if ASSERTIONS:  # pragma: no branch
                assert any(child is self for child in parentchildren), "Tree is corrupt."  # pragma: no cover
            # ATOMIC START
            parent.__children = [child for child in parentchildren if child is not self]
            self.__parent: NodeT_co | None = None
            # ATOMIC END
            self._post_detach(parent)

    def __attach(self, parent: NodeT_co | None) -> None:
        # pylint: disable=W0212
        if parent is not None:
            self._pre_attach(parent)
            parentchildren = parent.__children_or_empty
            if ASSERTIONS:  # pragma: no branch
                assert not any(child is self for child in parentchildren), "Tree is corrupt."  # pragma: no cover
            # ATOMIC START
            parentchildren.append(self)
            self.__parent = parent
            # ATOMIC END
            self._post_attach(parent)

    @property
    def __children_or_empty(self) -> list[NodeT_co]:
        if not hasattr(self, "_LightNodeMixin__children"):
            self.__children: list[NodeT_co] = []
        return self.__children

    def __children_get(self) -> tuple[NodeT_co, ...]:
        return tuple(self.__children_or_empty)

    @staticmethod
    def __check_children(children: Iterable[object]) -> None:
        seen = set()
        for child in children:
            childid = id(child)
            if childid not in seen:
                seen.add(childid)
            else:
                msg = f"Cannot add node {child!r} multiple times as child."
                raise TreeError(msg)

    def __children_set(self, children: tuple[NodeT_co, ...]) -> None:
        # convert iterable to tuple
        children = tuple(children)
        self.__check_children(children)
        # ATOMIC start
        old_children = self.children
        del self.children
        try:
            self._pre_attach_children(children)
            for child in children:
                child.parent = self
            self._post_attach_children(children)
            if ASSERTIONS:  # pragma: no branch
                assert len(self.children) == len(children)
        except Exception:
            self.children = old_children
            raise
        # ATOMIC end

    def __children_del(self) -> None:
        children = self.children
        self._pre_detach_children(children)
        for child in self.children:
            child.parent = None
        if ASSERTIONS:  # pragma: no branch
            assert len(self.children) == 0
        self._post_detach_children(children)

    children = property(
        __children_get,
        __children_set,
        __children_del,
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
        """,
    )

    def _pre_detach_children(self, children: tuple[NodeT_co, ...]) -> None:
        """Method call before detaching `children`."""

    def _post_detach_children(self, children: tuple[NodeT_co, ...]) -> None:
        """Method call after detaching `children`."""

    def _pre_attach_children(self, children: tuple[NodeT_co, ...]) -> None:
        """Method call before attaching `children`."""

    def _post_attach_children(self, children: tuple[NodeT_co, ...]) -> None:
        """Method call after attaching `children`."""

    @property
    def path(self) -> tuple[NodeT_co, ...]:
        """
        Path from root node down to this `Node`.

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

    def iter_path_reverse(self) -> Generator[NodeT_co, None, None]:
        """
        Iterate up the tree from the current node to the root node.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> for node in udo.iter_path_reverse():
        ...     print(node)
        Node('/Udo')
        >>> for node in marc.iter_path_reverse():
        ...     print(node)
        Node('/Udo/Marc')
        Node('/Udo')
        >>> for node in lian.iter_path_reverse():
        ...     print(node)
        Node('/Udo/Marc/Lian')
        Node('/Udo/Marc')
        Node('/Udo')
        """
        node: NodeT_co | None = cast("NodeT_co", self)
        while node is not None:
            yield node
            node = node.parent

    @property
    def _path(self) -> tuple[NodeT_co, ...]:
        return tuple(reversed(list(self.iter_path_reverse())))

    @property
    def ancestors(self) -> tuple[NodeT_co, ...]:
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
        if self.parent is None:
            return ()
        return self.parent.path

    @property
    def descendants(self) -> tuple[NodeT_co, ...]:
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
    def root(self) -> NodeT_co:
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
        node: NodeT_co = cast("NodeT_co", self)
        while node.parent is not None:
            node = node.parent
        return node

    @property
    def siblings(self) -> tuple[NodeT_co, ...]:
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
            return ()
        return tuple(node for node in parent.children if node is not self)

    @property
    def leaves(self) -> tuple[NodeT_co, ...]:
        """
        Tuple of all leaf nodes.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> loui = Node("Loui", parent=marc)
        >>> lazy = Node("Lazy", parent=marc)
        >>> udo.leaves
        (Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Loui'), Node('/Udo/Marc/Lazy'))
        >>> marc.leaves
        (Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Loui'), Node('/Udo/Marc/Lazy'))
        """
        return tuple(PreOrderIter(self, filter_=lambda node: node.is_leaf))

    @property
    def is_leaf(self) -> bool:
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
        return len(self.__children_or_empty) == 0

    @property
    def is_root(self) -> bool:
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
    def height(self) -> int:
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
        children = self.__children_or_empty
        if children:
            return max(child.height for child in children) + 1
        return 0

    @property
    def depth(self) -> int:
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
        # count without storing the entire path
        # pylint: disable=W0631
        for depth, _ in enumerate(self.iter_path_reverse()):
            continue
        return depth

    @property
    def size(self) -> int:
        """
        Tree size --- the number of nodes in tree starting at this node.

        >>> from anytree import Node
        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> loui = Node("Loui", parent=marc)
        >>> soe = Node("Soe", parent=lian)
        >>> udo.size
        5
        >>> marc.size
        4
        >>> lian.size
        2
        >>> loui.size
        1
        """
        # count without storing the entire path
        # pylint: disable=W0631
        for size, _ in enumerate(PreOrderIter(self), 1):
            continue
        return size

    def _pre_detach(self, parent: NodeMixin[NodeT_co] | LightNodeMixin[NodeT_co]) -> None:
        """Method call before detaching from `parent`."""

    def _post_detach(self, parent: NodeMixin[NodeT_co] | LightNodeMixin[NodeT_co]) -> None:
        """Method call after detaching from `parent`."""

    def _pre_attach(self, parent: NodeT_co | None) -> None:
        """Method call before attaching to `parent`."""

    def _post_attach(self, parent: NodeT_co | None) -> None:
        """Method call after attaching to `parent`."""
