from shutil import which

from pytest import mark
from test2ref import assert_refdata

from anytree import Node
from anytree.dotexport import RenderTreeGraph


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

    RenderTreeGraph(root).to_dotfile(tmp_path / "tree1.dot")
    assert_refdata(test_tree1, tmp_path)


def test_tree2(tmp_path):
    """Tree2."""
    root = Node("root")
    s0 = Node("sub0", parent=root, edge=2)
    Node("sub0B", parent=s0, foo=4, edge=109)
    Node("sub0A", parent=s0, edge="")
    s1 = Node("sub1", parent=root, edge="")
    Node("sub1A", parent=s1, edge=7)
    Node("sub1B", parent=s1, edge=8)
    s1c = Node("sub1C", parent=s1, edge=22)
    Node("sub1Ca", parent=s1c, edge=42)

    def nodenamefunc(node):
        return f"{node.name}:{node.depth}"

    def edgeattrfunc(node, child):
        return f'label="{node.name}:{child.name}"'

    r = RenderTreeGraph(
        root,
        options=["rankdir=LR;"],
        nodenamefunc=nodenamefunc,
        nodeattrfunc=lambda node: "shape=box",
        edgeattrfunc=edgeattrfunc,
    )

    r.to_dotfile(tmp_path / "tree2.dot")
    assert_refdata(test_tree2, tmp_path)


@mark.skipif(which("dot") is None, reason="requires graphviz`s `dot` command")
def test_tree_png(tmp_path):
    """Tree to png."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    Node("sub0B", parent=s0)
    Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    Node("sub1A", parent=s1)
    Node("sub1B", parent=s1)
    s1c = Node("sub1C", parent=s1)
    Node("sub1Ca", parent=s1c)

    RenderTreeGraph(root).to_picture(tmp_path / "tree1.png")
