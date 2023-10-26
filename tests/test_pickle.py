# -*- coding: utf-8 -*-
import pickle

from anytree import AnyNode, LoopError, Node, NodeMixin, PostOrderIter, PreOrderIter, RenderTree, SymlinkNode, TreeError


def test_pickle(tmp_path):
    """Pickling Compatibilty."""
    root = Node(name="root")
    a = Node(name="a", parent=root)
    b = Node(name="b", parent=a)
    c = SymlinkNode(target=b, parent=a)

    lines = str(RenderTree(root)).splitlines()
    assert lines == [
        "Node('/root')",
        "└── Node('/root/a')",
        "    ├── Node('/root/a/b')",
        "    └── SymlinkNode(Node('/root/a/b'))",
    ]

    filepath = tmp_path / "test.pkl"
    with open(filepath, "wb") as file:
        pickle.dump(root, file)

    with open(filepath, "rb") as file:
        loaded = pickle.load(file)

    assert str(RenderTree(root)).splitlines() == lines
