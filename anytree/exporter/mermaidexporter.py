import codecs
import logging
import re
from os import path, remove
from subprocess import check_call
from tempfile import NamedTemporaryFile

import six

from anytree import PreOrderIter

_RE_ESC = re.compile(r'["\\]')


class MermaidExporter:
    def __init__(
        self,
        node,
        graph="graph",
        name="TD",
        options=None,
        indent=0,
        nodenamefunc=None,
        nodeattrfunc=None,
        edgeattrfunc=None,
        edgetypefunc=None,
        maxlevel=None,
    ):
        """
        Mermaid Exporter.

        Args:
            node (Node): start node.

        Keyword Args:
            graph: Mermaid graph type.

            name: Mermaid graph name.

            options: list of options added to the graph.

            indent (int): number of spaces for indent.

            nodenamefunc: Function to extract node name from `node` object.
                          The function shall accept one `node` object as
                          argument and return the name of it.

            nodeattrfunc: Function to decorate a node with attributes.
                          The function shall accept one `node` object as
                          argument and return the attributes.

            edgeattrfunc: Function to decorate a edge with attributes.
                          The function shall accept two `node` objects as
                          argument. The first the node and the second the child
                          and return the attributes.

            edgetypefunc: Function to which gives the edge type.
                          The function shall accept two `node` objects as
                          argument. The first the node and the second the child
                          and return the edge (i.e. '->').

            maxlevel (int): Limit export to this number of levels.

        >>> from anytree import Node
        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root, edge=2)
        >>> s0b = Node("sub0B", parent=s0, foo=4, edge=109)
        >>> s0a = Node("sub0A", parent=s0, edge="")
        >>> s1 = Node("sub1", parent=root, edge="")
        >>> s1a = Node("sub1A", parent=s1, edge=7)
        >>> s1b = Node("sub1B", parent=s1, edge=8)
        >>> s1c = Node("sub1C", parent=s1, edge=22)
        >>> s1ca = Node("sub1Ca", parent=s1c, edge=42)

        A directed graph:

        >>> from anytree.exporter import MermaidExporter
        >>> for line in MermaidExporter(root):
        ...     print(line)
        graph TD
        A[root] --> B[sub0]
        A[root] --> C[sub1]
        B[sub0] --> D[sub0B]
        B[sub0] --> E[sub0A]
        C[sub1] --> F[sub1A]
        C[sub1] --> G[sub1B]
        C[sub1] --> H[sub1C]
        H[sub1C] --> I[sub1Ca]
        """
        self.node = node
        self.graph = graph
        self.name = name
        self.options = options
        self.indent = indent
        self.nodenamefunc = nodenamefunc
        self.nodeattrfunc = nodeattrfunc
        self.edgeattrfunc = edgeattrfunc
        self.edgetypefunc = edgetypefunc
        self.maxlevel = maxlevel

    def __iter__(self):
        # prepare
        indent = " " * self.indent
        nodenamefunc = self.nodenamefunc or self._default_nodenamefunc
        nodeattrfunc = self.nodeattrfunc or self._default_nodeattrfunc
        edgeattrfunc = self.edgeattrfunc or self._default_edgeattrfunc
        edgetypefunc = self.edgetypefunc or self._default_edgetypefunc
        return self.__iter(indent, nodenamefunc, nodeattrfunc, edgeattrfunc, edgetypefunc)

    @staticmethod
    def _default_nodenamefunc(node):
        return node.name

    @staticmethod
    def _default_nodeattrfunc(node):
        # pylint: disable=W0613
        return None

    @staticmethod
    def _default_edgeattrfunc(node, child):
        # pylint: disable=W0613
        return None

    @staticmethod
    def _default_edgetypefunc(node, child):
        # pylint: disable=W0613
        return "->"

    def __iter(self, indent, nodenamefunc, nodeattrfunc, edgeattrfunc, edgetypefunc):
        yield "{self.graph} {self.name}".format(self=self)
        for option in self.__iter_options(indent):
            yield option
        for node in self.__iter_nodes(indent, nodenamefunc, nodeattrfunc):
            yield node
        yield ""

    def __iter_options(self, indent):
        options = self.options
        if options:
            for option in options:
                yield "%s%s" % (indent, option)

    def __iter_nodes(self, indent, nodenamefunc, nodeattrfunc):
        def get_key(letter_index):
            return chr(65 + letter_index)

        index = 0
        for node in PreOrderIter(self.node, maxlevel=self.maxlevel):
            node.key = get_key(index)
            index += 1

        for node in PreOrderIter(self.node, maxlevel=self.maxlevel):
            nodekey = node.key
            nodename = nodenamefunc(node)
            nodeattr = nodeattrfunc(node)
            nodeattr = "|%s|" % nodeattr if nodeattr is not None else ""
            if node.parent is None:
                yield '%s%s[%s]' % (indent, nodekey, MermaidExporter.esc(nodename))
            else:
                yield '%s%s[%s] -->%s %s[%s]' % (indent, node.parent.key, MermaidExporter.esc(nodenamefunc(node.parent)),
                                            nodeattr, nodekey, MermaidExporter.esc(nodename))

    def to_markdown_file(self, filename):
        """
        Write graph to `filename`.

        >>> from anytree import Node
        >>> root = Node("root")
        >>> s0 = Node("sub0", parent=root)
        >>> s0b = Node("sub0B", parent=s0)
        >>> s0a = Node("sub0A", parent=s0)
        >>> s1 = Node("sub1", parent=root)
        >>> s1a = Node("sub1A", parent=s1)
        >>> s1b = Node("sub1B", parent=s1)
        >>> s1c = Node("sub1C", parent=s1)
        >>> s1ca = Node("sub1Ca", parent=s1c)

        >>> from anytree.exporter import MermaidExporter
        >>> MermaidExporter(root).to_markdown_file("tree.md")
        """
        with codecs.open(filename, "w", "utf-8") as file:
            file.write("```mermaid\n")
            for line in self:
                file.write("%s\n" % line)
            file.write("```")
            x = 1

    @staticmethod
    def esc(value):
        """Escape Strings."""
        return _RE_ESC.sub(lambda m: r"\%s" % m.group(0), six.text_type(value))

