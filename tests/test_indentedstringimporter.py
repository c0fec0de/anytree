# -*- coding: utf-8 -*-
from anytree import Node
from anytree import RenderTree
from anytree.importer import IndentedStringImporter


linelist = [
    "Node1",
    "Node2",
    "    Node3",
    "    Node4",
    "Node5",
    "    Node6",
    "        Node7",
    "    Node8",
    "        Node9",
    "       Node10",
    "      Node11",
    "     Node12",
    "    Node13",
    "   Node14",
    "  Node15",
    " Node16",
    "Node17"
]

expected_anynode = "\n".join([
    "AnyNode(name='root')",
    "├── AnyNode(name='Node1')",
    "├── AnyNode(name='Node2')",
    "│   ├── AnyNode(name='Node3')",
    "│   └── AnyNode(name='Node4')",
    "├── AnyNode(name='Node5')",
    "│   ├── AnyNode(name='Node6')",
    "│   │   └── AnyNode(name='Node7')",
    "│   ├── AnyNode(name='Node8')",
    "│   │   ├── AnyNode(name='Node9')",
    "│   │   ├── AnyNode(name='Node10')",
    "│   │   ├── AnyNode(name='Node11')",
    "│   │   └── AnyNode(name='Node12')",
    "│   ├── AnyNode(name='Node13')",
    "│   ├── AnyNode(name='Node14')",
    "│   ├── AnyNode(name='Node15')",
    "│   └── AnyNode(name='Node16')",
    "└── AnyNode(name='Node17')",
])


def test_indentedstring_importer_string():
    """Indented String Importer with whole string."""
    importer = IndentedStringImporter()
    data_string = "\n".join(linelist)
    root = importer.import_(data_string)
    r = RenderTree(root)
    assert str(r) == expected_anynode


def test_indentedstring_importer_list():
    """Indented String Importer with line list."""
    importer = IndentedStringImporter()
    root = importer.import_(linelist)
    r = RenderTree(root)
    assert str(r) == expected_anynode


def test_indentedstring_importer_node():
    """Indented String Importer using Node class."""
    importer = IndentedStringImporter(Node)
    data_string = "\n".join(linelist)
    root = importer.import_(data_string)
    r = RenderTree(root)
    expected = "\n".join([
        "Node('/root')",
        "├── Node('/root/Node1')",
        "├── Node('/root/Node2')",
        "│   ├── Node('/root/Node2/Node3')",
        "│   └── Node('/root/Node2/Node4')",
        "├── Node('/root/Node5')",
        "│   ├── Node('/root/Node5/Node6')",
        "│   │   └── Node('/root/Node5/Node6/Node7')",
        "│   ├── Node('/root/Node5/Node8')",
        "│   │   ├── Node('/root/Node5/Node8/Node9')",
        "│   │   ├── Node('/root/Node5/Node8/Node10')",
        "│   │   ├── Node('/root/Node5/Node8/Node11')",
        "│   │   └── Node('/root/Node5/Node8/Node12')",
        "│   ├── Node('/root/Node5/Node13')",
        "│   ├── Node('/root/Node5/Node14')",
        "│   ├── Node('/root/Node5/Node15')",
        "│   └── Node('/root/Node5/Node16')",
        "└── Node('/root/Node17')",
    ])
    assert str(r) == expected
