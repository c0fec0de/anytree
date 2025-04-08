from anytree import AnyNode, Node, NodeMixin
from anytree.exporter import DictExporter

from .helper import eq_


def test_dict_exporter():
    """Dict Exporter."""
    root = AnyNode(id="root")
    s0 = AnyNode(id="sub0", parent=root)
    s0b = AnyNode(id="sub0B", parent=s0)
    s0a = AnyNode(id="sub0A", parent=s0)
    s1 = AnyNode(id="sub1", parent=root, foo="bar")
    s1a = AnyNode(id="sub1A", parent=s1)
    s1b = AnyNode(id="sub1B", parent=s1)
    s1c = AnyNode(id="sub1C", parent=s1)
    s1ca = AnyNode(id="sub1Ca", parent=s1c)

    exporter = DictExporter()
    eq_(
        exporter.export(root),
        {
            "id": "root",
            "children": [
                {"id": "sub0", "children": [{"id": "sub0B"}, {"id": "sub0A"}]},
                {
                    "id": "sub1",
                    "foo": "bar",
                    "children": [{"id": "sub1A"}, {"id": "sub1B"}, {"id": "sub1C", "children": [{"id": "sub1Ca"}]}],
                },
            ],
        },
    )


def test_dict_exporter_node():
    """Dict Exporter."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root, foo="bar")
    s1a = Node("sub1A", parent=s1)
    s1b = Node("sub1B", parent=s1)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    exporter = DictExporter()
    eq_(
        exporter.export(root),
        {
            "name": "root",
            "children": [
                {"name": "sub0", "children": [{"name": "sub0B"}, {"name": "sub0A"}]},
                {
                    "name": "sub1",
                    "foo": "bar",
                    "children": [
                        {"name": "sub1A"},
                        {"name": "sub1B"},
                        {"name": "sub1C", "children": [{"name": "sub1Ca"}]},
                    ],
                },
            ],
        },
    )


def test_dict_exporter_filter():
    """Dict Exporter."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root, foo="bar")
    s1a = Node("sub1A", parent=s1)
    s1b = Node("sub1B", parent=s1)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    exporter = DictExporter(attriter=lambda attrs: [(k, v) for k, v in attrs if k == "name"])
    eq_(
        exporter.export(root),
        {
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
        },
    )


def test_dict_exporter_mixin():
    """Dict Exporter."""

    class MyClass(NodeMixin):
        def __init__(self, foo, parent=None):
            super().__init__()
            self.foo = foo
            self.parent = parent

    root = MyClass("root")
    s0 = MyClass("s0", parent=root)
    s0b = MyClass("s0b", parent=s0)
    s0a = MyClass("s0a", parent=s0)
    s1 = MyClass("s1", parent=root)
    s1a = MyClass("s1a", parent=s1)
    s1b = MyClass("s1b", parent=s1)
    s1c = MyClass("s1c", parent=s1)
    s1ca = MyClass("s1ca", parent=s1c)

    exporter = DictExporter()
    eq_(
        exporter.export(root),
        {
            "foo": "root",
            "children": [
                {"foo": "s0", "children": [{"foo": "s0b"}, {"foo": "s0a"}]},
                {
                    "foo": "s1",
                    "children": [{"foo": "s1a"}, {"foo": "s1b"}, {"foo": "s1c", "children": [{"foo": "s1ca"}]}],
                },
            ],
        },
    )
