# -*- coding: utf-8 -*-
import pathlib

from pytest import fixture

from anytree import Node
from anytree.exporter import DotExporter

REFDATA = pathlib.Path(__file__).parent / "refdata" / "test_dotexporter"


from .util import assert_gen


@fixture
def root():
    root = Node("root")
    s0 = Node("sub0", parent=root, edge=2)
    Node("sub0B", parent=s0, foo=4, edge=109)
    Node("sub0A", parent=s0, edge="")
    s1 = Node("sub1", parent=root, edge="")
    Node("sub1A", parent=s1, edge=7)
    Node('sub1"B', parent=s1, edge=8)
    s1c = Node("su\\b1C", parent=s1, edge=22)
    Node("sub1Ca", parent=s1c, edge=42)
    yield root


def test_tree(tmp_path, root):
    """Tree."""
    DotExporter(root).to_dotfile(tmp_path / "tree.md")
    assert_gen(tmp_path, REFDATA / "tree")


def test_tree_custom(tmp_path, root):
    """Tree Custom."""

    def nodenamefunc(node):
        return "%s:%s" % (node.name, node.depth)

    def edgeattrfunc(node, child):
        return 'label="%s:%s"' % (node.name, child.name)

    def nodefunc(node):
        return '("%s")' % (node.name)

    def edgefunc(node, child):
        return f"--{child.edge}-->"

    DotExporter(
        root,
        options=["rankdir=LR;"],
        nodenamefunc=nodenamefunc,
        nodeattrfunc=lambda node: "shape=box",
        edgeattrfunc=edgeattrfunc,
    ).to_dotfile(tmp_path / "tree_custom.md")
    assert_gen(tmp_path, REFDATA / "tree_custom")


def test_tree_filter(tmp_path, root):
    """Tree with Filter."""
    DotExporter(root, filter_=lambda node: node.name.startswith("sub")).to_dotfile(tmp_path / "tree_filter.md")
    assert_gen(tmp_path, REFDATA / "tree_filter")


def test_tree_stop(tmp_path, root):
    """Tree with stop."""
    DotExporter(root, stop=lambda node: node.name == "sub1").to_dotfile(tmp_path / "tree_stop.md")
    assert_gen(tmp_path, REFDATA / "tree_stop")


def test_tree_maxlevel(tmp_path, root):
    """Tree with maxlevel."""
    DotExporter(root, maxlevel=2).to_dotfile(tmp_path / "tree_maxlevel.md")
    assert_gen(tmp_path, REFDATA / "tree_maxlevel")


def test_esc():
    """Test proper escape of quotes."""
    n = Node(r'6"-6\"')
    assert tuple(DotExporter(n)) == (
        r"digraph tree {",
        r'    "6\"-6\\\"";',
        r"}",
    )
