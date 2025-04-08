from copy import deepcopy

from anytree import Node, RenderTree
from anytree.exporter import DictExporter
from anytree.importer import DictImporter

from .helper import eq_


def test_dict_importer():
    """Dict Importer."""
    importer = DictImporter()
    exporter = DictExporter()
    refdata = {
        "id": "root",
        "children": [
            {"id": "sub0", "children": [{"id": "sub0B"}, {"id": "sub0A"}]},
            {
                "id": "sub1",
                "children": [{"id": "sub1A"}, {"id": "sub1B"}, {"id": "sub1C", "children": [{"id": "sub1Ca"}]}],
            },
        ],
    }
    data = deepcopy(refdata)
    root = importer.import_(data)
    eq_(data, refdata)
    eq_(exporter.export(root), data)
    r = RenderTree(root)
    assert str(r).splitlines() == [
        "AnyNode(id='root')",
        "├── AnyNode(id='sub0')",
        "│   ├── AnyNode(id='sub0B')",
        "│   └── AnyNode(id='sub0A')",
        "└── AnyNode(id='sub1')",
        "    ├── AnyNode(id='sub1A')",
        "    ├── AnyNode(id='sub1B')",
        "    └── AnyNode(id='sub1C')",
        "        └── AnyNode(id='sub1Ca')",
    ]


def test_dict_importer_node():
    """Dict Importer."""
    importer = DictImporter(Node)
    exporter = DictExporter()
    refdata = {
        "name": "root",
        "children": [
            {"name": "sub0", "children": [{"name": "sub0B"}, {"name": "sub0A"}]},
            {
                "name": "sub1",
                "children": [
                    {"name": "sub1A"},
                    {"name": "sub1B"},
                    {"name": "sub1C", "children": [{"name": "sub1Ca"}]},
                ],
            },
        ],
    }
    data = deepcopy(refdata)
    root = importer.import_(data)
    eq_(data, refdata)
    eq_(exporter.export(root), data)
    r = RenderTree(root)
    assert str(r).splitlines() == [
        "Node('/root')",
        "├── Node('/root/sub0')",
        "│   ├── Node('/root/sub0/sub0B')",
        "│   └── Node('/root/sub0/sub0A')",
        "└── Node('/root/sub1')",
        "    ├── Node('/root/sub1/sub1A')",
        "    ├── Node('/root/sub1/sub1B')",
        "    └── Node('/root/sub1/sub1C')",
        "        └── Node('/root/sub1/sub1C/sub1Ca')",
    ]
