# -*- coding: utf-8 -*-
"""
Tree Rendering.

* :any:`RenderTree` using the following styles:
    * :any:`AsciiStyle`
    * :any:`ContStyle`
    * :any:`ContRoundStyle`
    * :any:`DoubleStyle`
"""

import collections

import six


Row = collections.namedtuple("Row", ("pre", "fill", "node"))


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

        >>> from anytree import Node, RenderTree
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

        >>> from anytree import Node, RenderTree
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

        >>> from anytree import Node, RenderTree
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

        >>> from anytree import Node, RenderTree
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

        >>> from anytree import Node, RenderTree
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

        >>> for row in RenderTree(root, childiter=reversed):
        ...     print("%s%s" % (row.pre, row.node.name))
        root
        ├── sub1
        └── sub0
            ├── sub0A
            └── sub0B

        Or writing your own sort function:

        >>> def mysort(items):
        ...     return sorted(items, key=lambda item: item.name)
        >>> for row in RenderTree(root, childiter=mysort):
        ...     print("%s%s" % (row.pre, row.node.name))
        root
        ├── sub0
        │   ├── sub0A
        │   └── sub0B
        └── sub1

        :any:`by_attr` simplifies attribute rendering and supports multiline:

        >>> print(RenderTree(root).by_attr())
        root
        ├── sub0
        │   ├── sub0B
        │   └── sub0A
        └── sub1
        >>> print(RenderTree(root).by_attr("lines"))
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
        """
        if not isinstance(style, AbstractStyle):
            style = style()
        self.node = node
        self.style = style
        self.childiter = childiter

    def __iter__(self):
        return self.__next(self.node, tuple())

    def __next(self, node, continues):
        yield RenderTree.__item(node, continues, self.style)
        children = node.children
        if children:
            lastidx = len(children) - 1
            for idx, child in enumerate(self.childiter(children)):
                for grandchild in self.__next(child, continues + (idx != lastidx, )):
                    yield grandchild

    @staticmethod
    def __item(node, continues, style):
        if not continues:
            return Row(u'', u'', node)
        else:
            items = [style.vertical if cont else style.empty for cont in continues]
            indent = ''.join(items[:-1])
            branch = style.cont if continues[-1] else style.end
            pre = indent + branch
            fill = ''.join(items)
            return Row(pre, fill, node)

    def __str__(self):
        lines = ["%s%r" % (pre, node) for pre, _, node in self]
        return "\n".join(lines)

    def __repr__(self):
        classname = self.__class__.__name__
        args = [repr(self.node),
                "style=%s" % repr(self.style),
                "childiter=%s" % repr(self.childiter)]
        return "%s(%s)" % (classname, ", ".join(args))

    def by_attr(self, attrname="name"):
        """Return rendered tree with node attribute `attrname`."""
        def get():
            for pre, fill, node in self:
                attr = getattr(node, attrname, "")
                if isinstance(attr, (list, tuple)):
                    lines = attr
                else:
                    lines = str(attr).split("\n")
                yield u"%s%s" % (pre, lines[0])
                for line in lines[1:]:
                    yield u"%s%s" % (fill, line)
        return "\n".join(get())
