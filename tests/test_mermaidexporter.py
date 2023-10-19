# -*- coding: utf-8 -*-

import pathlib

from anytree import Node
from anytree.exporter import MermaidExporter

REFDATA = pathlib.Path(__file__).parent / "refdata" / "test_mermaidexporter"


from .util import assert_gen


def test_tree1(tmp_path):
    """Tree1."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    Node("sub0B", parent=s0)
    Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    Node("sub1A", parent=s1)
    Node("sub1B", parent=s1)
    s1c = Node("sub1C", parent=s1)
    Node(99, parent=s1c)

    MermaidExporter(root).to_markdown_file(tmp_path / "tree1.md")
    assert_gen(tmp_path, REFDATA / "tree1")


def test_tree2(tmp_path):
    """Tree2."""
    root = Node("root")
    s0 = Node("sub0", parent=root, edge=2)
    Node("sub0B", parent=s0, foo=4, edge=109)
    Node("sub0A", parent=s0, edge="")
    s1 = Node("sub1", parent=root, edge="")
    Node("sub1A", parent=s1, edge=7)
    Node('su"b"1B', parent=s1, edge=8)
    s1c = Node("su\\b1C", parent=s1, edge=22)
    Node("sub1Ca", parent=s1c, edge=42)

    def nodefunc(node):
        return '("%s")' % (node.name)

    def edgefunc(node, child):
        return f"--{child.edge}-->"

    options = [
        "%% just an example comment",
        "%% could be an option too",
    ]

    MermaidExporter(
        root,
        options=options,
        nodefunc=nodefunc,
        edgefunc=edgefunc,
    ).to_markdown_file(tmp_path / "tree2.md")
    assert_gen(tmp_path, REFDATA / "tree2")
