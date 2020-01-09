# -*- coding: utf-8 -*-
from copy import deepcopy

from nose.tools import eq_

from anytree import Node
from anytree import RenderTree
from anytree.exporter import DictExporter
from anytree.importer import DictImporter
from helper import eq_str


def test_dict_importer():
    """Dict Importer."""
    importer = DictImporter()
    exporter = DictExporter()
    refdata = {
        'id': 'root', 'children': [
            {'id': 'sub0', 'children': [
                {'id': 'sub0B'},
                {'id': 'sub0A'}
            ]},
            {'id': 'sub1', 'children': [
                {'id': 'sub1A'},
                {'id': 'sub1B'},
                {'id': 'sub1C', 'children': [
                    {'id': 'sub1Ca'}
                ]}
            ]}
        ]}
    data = deepcopy(refdata)
    root = importer.import_(data)
    eq_(data, refdata)
    eq_(exporter.export(root), data)
    r = RenderTree(root)
    expected = u"\n".join([
        u"AnyNode(id='root')",
        u"├── AnyNode(id='sub0')",
        u"│   ├── AnyNode(id='sub0B')",
        u"│   └── AnyNode(id='sub0A')",
        u"└── AnyNode(id='sub1')",
        u"    ├── AnyNode(id='sub1A')",
        u"    ├── AnyNode(id='sub1B')",
        u"    └── AnyNode(id='sub1C')",
        u"        └── AnyNode(id='sub1Ca')",
    ])
    eq_str(str(r), expected)


def test_dict_importer_node():
    """Dict Importer."""
    importer = DictImporter(Node)
    exporter = DictExporter()
    refdata = {
        'name': 'root', 'children': [
            {'name': 'sub0', 'children': [
                {'name': 'sub0B'},
                {'name': 'sub0A'}
            ]},
            {'name': 'sub1', 'children': [
                {'name': 'sub1A'},
                {'name': 'sub1B'},
                {'name': 'sub1C', 'children': [
                    {'name': 'sub1Ca'}
                ]}
            ]}
        ]}
    data = deepcopy(refdata)
    root = importer.import_(data)
    eq_(data, refdata)
    eq_(exporter.export(root), data)
    r = RenderTree(root)
    expected = u"\n".join([
        u"Node('/root')",
        u"├── Node('/root/sub0')",
        u"│   ├── Node('/root/sub0/sub0B')",
        u"│   └── Node('/root/sub0/sub0A')",
        u"└── Node('/root/sub1')",
        u"    ├── Node('/root/sub1/sub1A')",
        u"    ├── Node('/root/sub1/sub1B')",
        u"    └── Node('/root/sub1/sub1C')",
        u"        └── Node('/root/sub1/sub1C/sub1Ca')",
    ])
    eq_str(str(r), expected)
