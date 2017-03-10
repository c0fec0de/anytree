# -*- coding: utf-8 -*-
"""
Powerful and Lightweight Python Tree Data Structure.

Overview
~~~~~~~~

The :any:`anytree` API is splitted into the following parts:

* Node classes:
    * :any:`Node`: a simple tree node
    * :any:`NodeMixin`: extends any python class to a tree node.

# Node resolution:
    * :any:`Resolver`: retrieve node via absolute or relative path.

* Tree Traversal strategies:
    * :any:`PreOrderIter`: iterate over tree using pre-order strategy
    * :any:`PostOrderIter`: iterate over tree using post-order strategy

* Tree Rendering:
    * :any:`RenderTree` using the following styles:
        * :any:`AsciiStyle`
        * :any:`ContStyle`
        * :any:`ContRoundStyle`
        * :any:`DoubleStyle`

Classes
~~~~~~~
"""

from __future__ import print_function
import collections
import six


class NodeMixin(object):

    u"""
    The :any:`NodeMixin` class extends any Python class to a tree node.

    The only tree relevant information is the `parent` attribute.
    If `None` the :any:`NodeMixin` is root node.
    If set to another node, the :any:`NodeMixin` becomes the child of it.

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

        >>> udo = Node("Udo")
        >>> marc = Node("Marc")
        >>> lian = Node("Lian", parent=marc)
        >>> print(RenderTree(udo))
        Node('/Udo')
        >>> print(RenderTree(marc))
        Node('/Marc')
        └── Node('/Marc/Lian')

        Attach:

        >>> marc.parent = udo
        >>> print(RenderTree(udo))
        Node('/Udo')
        └── Node('/Udo/Marc')
            └── Node('/Udo/Marc/Lian')

        To make a node to a root node, just set this attribute to `None`.
        """
        try:
            return self._parent
        except AttributeError:
            return None

    @parent.setter
    def parent(self, value):
        try:
            parent = self._parent
        except AttributeError:
            parent = None
        if value is None:
            # make this Node to root node
            if parent:
                # unregister at parent
                parentchildren = parent._children
                assert self in parentchildren, "Tree internal data is corrupt."
                parentchildren.remove(self)
        elif parent is not value:
            # change parent node
            if parent:
                parentchildren = parent._children
                # unregister at old parent
                assert self in parentchildren, "Tree internal data is corrupt."
                parentchildren.remove(self)
            # check for loop
            if value is self:
                msg = "Cannot set parent. %r cannot be parent of itself."
                raise LoopError(msg % self)
            if self in value.path:
                msg = "Cannot set parent. %r is parent of %r."
                raise LoopError(msg % (self, value))

            # register at new parent
            parentchildren = value._children
            assert self not in parentchildren, "Tree internal data is corrupt."
            parentchildren.append(self)
        else:
            # keep parent
            pass
        # apply
        self._parent = value

    @property
    def _children(self):
        try:
            return self.__children
        except AttributeError:
            self.__children = []
            return self.__children

    @property
    def children(self):
        """
        All child nodes.

        >>> dan = Node("Dan")
        >>> jet = Node("Jet", parent=dan)
        >>> jan = Node("Jan", parent=dan)
        >>> joe = Node("Joe", parent=dan)
        >>> dan.children
        (Node('/Dan/Jet'), Node('/Dan/Jan'), Node('/Dan/Joe'))
        """
        return tuple(self._children)

    @property
    def path(self):
        """
        Path of this `Node`.

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
    def anchestors(self):
        """
        All parent nodes and their parent nodes.

        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> udo.anchestors
        ()
        >>> marc.anchestors
        (Node('/Udo'),)
        >>> lian.anchestors
        (Node('/Udo'), Node('/Udo/Marc'))
        """
        return self._path[:-1]

    @property
    def descendants(self):
        """
        All child nodes and all their child nodes.

        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> loui = Node("Loui", parent=marc)
        >>> udo.descendants
        (Node('/Udo/Marc'), Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Loui'))
        >>> marc.descendants
        (Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Loui'))
        >>> lian.descendants
        ()
        """
        return tuple(PreOrderIter(self))[1:]

    @property
    def root(self):
        """
        Tree Root Node.

        >>> udo = Node("Udo")
        >>> marc = Node("Marc", parent=udo)
        >>> lian = Node("Lian", parent=marc)
        >>> udo.root is None
        True
        >>> marc.root
        Node('/Udo')
        >>> lian.root
        Node('/Udo')
        """
        if self.parent:
            return self._path[0]
        else:
            return None

    @property
    def siblings(self):
        """
        Tuple of nodes with the same parent.

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
            return tuple([node for node in parent._children if node != self])

    @property
    def is_leaf(self):
        """
        `Node` has no childrean (External Node).

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
        return len(self._children) == 0

    @property
    def is_root(self):
        """
        `Node` is tree root.

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
        if self._children:
            return max([child.height for child in self._children]) + 1
        else:
            return 0

    @property
    def depth(self):
        """
        Number of edges to the root `Node`.

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


class Node(NodeMixin, object):

    def __init__(self, name, parent=None, **kwargs):
        u"""
        A simple tree node with a `name` and any `kwargs`.

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
        self.name = name
        self.parent = parent
        self.__dict__.update(kwargs)

    @property
    def name(self):
        """Name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __repr__(self):
        classname = self.__class__.__name__
        args = ["%r" % "/".join([""] + [str(node.name) for node in self.path])]
        for key, value in filter(lambda item: not item[0].startswith("_"),
                                 sorted(self.__dict__.items(),
                                        key=lambda item: item[0])):
            args.append("%s=%r" % (key, value))
        return "%s(%s)" % (classname, ", ".join(args))


class Resolver(object):

    def __init__(self, pathattr='name'):
        """Resolve :any:`NodeMixin` paths using attribute `pathattr`."""
        super().__init__()
        self.pathattr = pathattr

    def get(self, node, path):
        """
        Return instance at `path`.

        An example module tree:

        >>> top = Node("top", parent=None)
        >>> sub0 = Node("sub0", parent=top)
        >>> sub0sub0 = Node("sub0sub0", parent=sub0)
        >>> sub0sub1 = Node("sub0sub1", parent=sub0)
        >>> sub1 = Node("sub1", parent=top)

        A resolver using the `name` attribute:

        >>> r = Resolver('name')

        Relative paths:

        >>> r.get(top, "sub0/sub0sub0")
        Node('/top/sub0/sub0sub0')
        >>> r.get(sub1, "..")
        Node('/top')
        >>> r.get(sub1, "../sub0/sub0sub1")
        Node('/top/sub0/sub0sub1')
        >>> r.get(sub1, ".")
        Node('/top/sub1')
        >>> r.get(sub1, "")
        Node('/top/sub1')
        >>> r.get(top, "sub2")
        Traceback (most recent call last):
          ...
        anytree.ResolverError: Node('/top') has no child sub2. Children are: 'sub0', 'sub1'.

        Absolute paths:

        >>> r.get(sub0sub0, "/top")
        Node('/top')
        >>> r.get(sub0sub0, "/top/sub0")
        Node('/top/sub0')
        >>> r.get(sub0sub0, "/")
        Traceback (most recent call last):
          ...
        anytree.ResolverError: root node needs to be specified '/top'.
        >>> r.get(sub0sub0, "/bar")
        Traceback (most recent call last):
          ...
        anytree.ResolverError: root node is named '/top', not '/bar'.
        """
        parts = path.split("/")
        if path.startswith("/"):
            node = node.root
            rootpart = self._get_part(node)
            parts.pop(0)
            if not parts[0]:
                msg = "root node needs to be specified '/%s'."
                raise ResolverError(node, "", msg % str(rootpart))
            elif parts[0] != rootpart:
                msg = "root node is named '/%s', not '/%s'."
                raise ResolverError(node, "", msg % (str(rootpart), parts[0]))
            parts.pop(0)
        for part in parts:
            if part == "..":
                node = node.parent
            elif part in ("", "."):
                pass
            else:
                subnodes = [(self._get_part(child), child)
                            for child in node.children]
                nodemap = collections.OrderedDict(subnodes)
                try:
                    node = nodemap[part]
                except KeyError:
                    names = ", ".join([repr(key) for key in nodemap.keys()])
                    msg = "%r has no child %s. Children are: %s."
                    msg = msg % (node, part, names)
                    raise ResolverError(node, part, msg) from None
        return node

    def _get_part(self, node):
        return getattr(node, self.pathattr)


class ResolverError(RuntimeError):

    def __init__(self, node, child, msg):
        """Resolver Error at `node` handling `child`."""
        super(ResolverError, self).__init__(msg)
        self.node = node
        self.child = child


class PreOrderIter(object):

    def __init__(self, node):
        """
        Iterate over tree applying pre-order strategy starting at `node`.

        >>> f = Node("f")
        >>> b = Node("b", parent=f)
        >>> a = Node("a", parent=b)
        >>> d = Node("d", parent=b)
        >>> c = Node("c", parent=d)
        >>> e = Node("e", parent=d)
        >>> g = Node("g", parent=f)
        >>> i = Node("i", parent=g)
        >>> h = Node("h", parent=i)

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

        >>> f = Node("f")
        >>> b = Node("b", parent=f)
        >>> a = Node("a", parent=b)
        >>> d = Node("d", parent=b)
        >>> c = Node("c", parent=d)
        >>> e = Node("e", parent=d)
        >>> g = Node("g", parent=f)
        >>> i = Node("i", parent=g)
        >>> h = Node("h", parent=i)

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


class AbstractStyle(object):

    def __init__(self, vertical, cont, end):
        """
        Tree Render Style.

        Args:

            vertical: Sign for vertical line.

            cont: Chars for a continued branch.

            end: Chars for the last branch.
        """
        super(AbstractStyle, self).__init__()
        self.vertical = vertical
        self.cont = cont
        self.end = end
        assert (len(cont) == len(vertical) and len(cont) == len(end)), (
            "'%s', '%s' and '%s' need to have equal length" % (vertical, cont,
                                                               end))

    @property
    def empty(self):
        """Empty string as placeholder."""
        return ' ' * len(self.end)

    def __repr__(self):
        classname = self.__class__.__name__
        return "%s()" % classname


class AsciiStyle(AbstractStyle):

    def __init__(self):
        """
        Ascii style.

        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root)
        >>> s0b = Node("sub0B", parent=s0)
        >>> s0a = Node("sub0A", parent=s0)
        >>> s1 = Node("sub1", parent=root)

        >>> print(RenderTree(root, style=AsciiStyle()))
        Node('/root')
        |-- Node('/root/sub0')
        |   |-- Node('/root/sub0/sub0B')
        |   +-- Node('/root/sub0/sub0A')
        +-- Node('/root/sub1')
        """
        super(AsciiStyle, self).__init__(u'|   ', u'|-- ', u'+-- ')


class ContStyle(AbstractStyle):

    def __init__(self):
        u"""
        Continued style, without gaps.

        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root)
        >>> s0b = Node("sub0B", parent=s0)
        >>> s0a = Node("sub0A", parent=s0)
        >>> s1 = Node("sub1", parent=root)

        >>> print(RenderTree(root, style=ContStyle()))
        Node('/root')
        ├── Node('/root/sub0')
        │   ├── Node('/root/sub0/sub0B')
        │   └── Node('/root/sub0/sub0A')
        └── Node('/root/sub1')
        """
        super(ContStyle, self).__init__(u'\u2502   ',
                                        u'\u251c\u2500\u2500 ',
                                        u'\u2514\u2500\u2500 ')


class ContRoundStyle(AbstractStyle):

    def __init__(self):
        u"""
        Continued style, without gaps, round edges.

        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root)
        >>> s0b = Node("sub0B", parent=s0)
        >>> s0a = Node("sub0A", parent=s0)
        >>> s1 = Node("sub1", parent=root)

        >>> print(RenderTree(root, style=ContRoundStyle()))
        Node('/root')
        ├── Node('/root/sub0')
        │   ├── Node('/root/sub0/sub0B')
        │   ╰── Node('/root/sub0/sub0A')
        ╰── Node('/root/sub1')
        """
        super(ContRoundStyle, self).__init__(u'\u2502   ',
                                             u'\u251c\u2500\u2500 ',
                                             u'\u2570\u2500\u2500 ')


class DoubleStyle(AbstractStyle):

    def __init__(self):
        u"""
        Double line style, without gaps.

        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root)
        >>> s0b = Node("sub0B", parent=s0)
        >>> s0a = Node("sub0A", parent=s0)
        >>> s1 = Node("sub1", parent=root)

        >>> print(RenderTree(root, style=DoubleStyle))
        Node('/root')
        ╠══ Node('/root/sub0')
        ║   ╠══ Node('/root/sub0/sub0B')
        ║   ╚══ Node('/root/sub0/sub0A')
        ╚══ Node('/root/sub1')

        """
        super(DoubleStyle, self).__init__(u'\u2551   ',
                                          u'\u2560\u2550\u2550 ',
                                          u'\u255a\u2550\u2550 ')


@six.python_2_unicode_compatible
class RenderTree(object):

    def __init__(self, node, style=ContStyle(), childiter=list):
        u"""
        Render tree starting at `node`.

        Keyword Args:
            style (AbstractStyle): Render Style.

            childiter: Child iterator.

        :any:`RenderTree` is an iterator, returning a tuple with 3 items:

        `pre`
            tree prefix.

        `fill`
            filling for multiline entries.

        `node`
            :any:`NodeMixin` object.

        It is up to the user to assemble these parts to a whole.

        >>> root = Node("root", lines=["c0fe", "c0de"])
        >>> s0 = Node("sub0", parent=root, lines=["ha", "ba"])
        >>> s0b = Node("sub0B", parent=s0, lines=["1", "2", "3"])
        >>> s0a = Node("sub0A", parent=s0, lines=["a", "b"])
        >>> s1 = Node("sub1", parent=root, lines=["Z"])

        Simple one line:

        >>> for pre, _, node in RenderTree(root):
        ...     print("%s%s" % (pre, node.name))
        root
        ├── sub0
        │   ├── sub0B
        │   └── sub0A
        └── sub1

        Multiline:

        >>> for pre, fill, node in RenderTree(root):
        ...     print("%s%s" % (pre, node.lines[0]))
        ...     for line in node.lines[1:]:
        ...         print("%s%s" % (fill, line))
        c0fe
        c0de
        ├── ha
        │   ba
        │   ├── 1
        │   │   2
        │   │   3
        │   └── a
        │       b
        └── Z

        The `childiter` is responsible for iterating over child nodes at the
        same level. An reversed order can be achived by using `reversed`.

        >>> for pre, _, node in RenderTree(root, childiter=reversed):
        ...     print("%s%s" % (pre, node.name))
        root
        ├── sub1
        └── sub0
            ├── sub0A
            └── sub0B

        Or writing your own sort function:

        >>> def mysort(items):
        ...     return sorted(items, key=lambda item: item.name)
        >>> for pre, _, node in RenderTree(root, childiter=mysort):
        ...     print("%s%s" % (pre, node.name))
        root
        ├── sub0
        │   ├── sub0A
        │   └── sub0B
        └── sub1
        """
        if not isinstance(style, AbstractStyle):
            style = style()
        self.node = node
        self.style = style
        self.childiter = childiter

    def __iter__(self):
        return self.__next(self.node, tuple())

    def __next(self, node, continues):
        # item
        if not continues:
            yield u'', u'', node
        else:
            style = self.style
            indent = ''.join([style.vertical if cont else style.empty
                              for cont in continues[:-1]])
            branch = style.cont if continues[-1] else style.end
            pre = indent + branch
            fill = ''.join([style.vertical if cont else style.empty
                            for cont in continues])
            yield pre, fill, node
        # children
        children = node.children
        if children:
            lastidx = len(children) - 1
            for idx, child in enumerate(self.childiter(children)):
                for grandchild in self.__next(child,
                                              continues + (idx != lastidx, )):
                    yield grandchild

    def __str__(self):
        lines = ["%s%r" % (pre, node) for pre, _, node in self]
        return "\n".join(lines)

    def __repr__(self):
        classname = self.__class__.__name__
        args = [repr(self.node),
                "style=%s" % repr(self.style),
                "childiter=%s" % repr(self.childiter)]
        return "%s(%s)" % (classname, ", ".join(args))


class LoopError(RuntimeError):

    """Tree contains infinite loop."""

    pass
