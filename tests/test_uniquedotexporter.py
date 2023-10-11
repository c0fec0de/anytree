# -*- coding: utf-8 -*-
from filecmp import cmp
from os import makedirs
from os.path import dirname, exists, join
from shutil import rmtree

from helper import eq_, with_setup

from anytree import Node
from anytree.exporter import UniqueDotExporter


def test_tree1():
    """Tree1."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)

    lines = tuple(UniqueDotExporter(root))
    eq_(
        lines,
        (
            "digraph tree {",
            '    "0" [label="root"];',
            '    "1" [label="sub0"];',
            '    "2" [label="sub0B"];',
            '    "0" -> "1";',
            '    "1" -> "2";',
            "}",
        ),
    )
