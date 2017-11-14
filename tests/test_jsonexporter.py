from nose.tools import eq_

from anytree import AnyNode
from anytree.exporter import JsonExporter


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

    exporter = JsonExporter(indent=2, sort_keys=True)
    eq_(exporter.export(root), (
        '{\n'
        '  "children": [\n'
        '    {\n'
        '      "children": [\n'
        '        {\n'
        '          "id": "sub0B"\n'
        '        },\n'
        '        {\n'
        '          "id": "sub0A"\n'
        '        }\n'
        '      ],\n'
        '      "id": "sub0"\n'
        '    },\n'
        '    {\n'
        '      "children": [\n'
        '        {\n'
        '          "id": "sub1A"\n'
        '        },\n'
        '        {\n'
        '          "id": "sub1B"\n'
        '        },\n'
        '        {\n'
        '          "children": [\n'
        '            {\n'
        '              "id": "sub1Ca"\n'
        '            }\n'
        '          ],\n'
        '          "id": "sub1C"\n'
        '        }\n'
        '      ],\n'
        '      "id": "sub1"\n'
        '    }\n'
        '  ],\n'
        '  "id": "root"\n'
        '}'
    ))
