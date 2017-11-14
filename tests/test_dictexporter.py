from nose.tools import eq_

from anytree import AnyNode
from anytree.exporter import DictExporter


def test_dict_exporter():
    """Dict Exporter."""
    root = AnyNode(id="root")
    s0 = AnyNode(id="sub0", parent=root)
    s0b = AnyNode(id="sub0B", parent=s0)
    s0a = AnyNode(id="sub0A", parent=s0)
    s1 = AnyNode(id="sub1", parent=root)
    s1a = AnyNode(id="sub1A", parent=s1)
    s1b = AnyNode(id="sub1B", parent=s1)
    s1c = AnyNode(id="sub1C", parent=s1)
    s1ca = AnyNode(id="sub1Ca", parent=s1c)

    exporter = DictExporter()
    eq_(exporter.export(root),
        {'id': 'root', 'children': [
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
    )
