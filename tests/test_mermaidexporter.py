from pytest import fixture
from test2ref import assert_refdata

from anytree import Node
from anytree.exporter import MermaidExporter


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
    MermaidExporter(root).to_file(tmp_path / "tree.md")
    assert_refdata(test_tree, tmp_path)


def test_tree_custom(tmp_path, root):
    """Tree Custom."""

    def nodefunc(node):
        return f'("{node.name}")'

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
    ).to_file(tmp_path / "tree_custom.md")
    assert_refdata(test_tree_custom, tmp_path)


def test_tree_filter(tmp_path, root):
    """Tree with Filter."""
    MermaidExporter(root, filter_=lambda node: node.name.startswith("sub")).to_file(tmp_path / "tree_filter.md")
    assert_refdata(test_tree_filter, tmp_path)


def test_tree_stop(tmp_path, root):
    """Tree with stop."""
    MermaidExporter(root, stop=lambda node: node.name == "sub1").to_file(tmp_path / "tree_stop.md")
    assert_refdata(test_tree_stop, tmp_path)


def test_tree_maxlevel(tmp_path, root):
    """Tree with maxlevel."""
    MermaidExporter(root, maxlevel=2).to_file(tmp_path / "tree_maxlevel.md")
    assert_refdata(test_tree_maxlevel, tmp_path)
