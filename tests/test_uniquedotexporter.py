# -*- coding: utf-8 -*-
from filecmp import cmp
from os import makedirs
from os.path import dirname
from os.path import exists
from os.path import join
from shutil import rmtree

from nose.tools import eq_
from nose.tools import with_setup

from anytree import Node
from anytree.exporter import UniqueDotExporter


def test_tree1():
    """Tree1."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)

    id_root = hex(id(root))
    id_s0 = hex(id(s0))
    id_s0b = hex(id(s0b))

    lines = tuple(UniqueDotExporter(root))
    eq_(lines, ('digraph tree {',
                '    "{id_root}" [label="root"];'.format(id_root=id_root),
                '    "{id_s0}" [label="sub0"];'.format(id_s0=id_s0),
                '    "{id_s0b}" [label="sub0B"];'.format(id_s0b=id_s0b),
                '    "{id_root}" -> "{id_s0}";'.format(id_root=id_root, id_s0=id_s0),
                '    "{id_s0}" -> "{id_s0b}";'.format(id_s0=id_s0, id_s0b=id_s0b),
                '}'))
