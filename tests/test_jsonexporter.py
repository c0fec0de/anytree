import filecmp
import os

from tempfile import TemporaryDirectory

from nose.tools import eq_

from anytree import AnyNode
from anytree.exporter import JsonExporter


def test_json_exporter():
    """Json Exporter."""
    root = AnyNode(id="root")
    s0 = AnyNode(id="sub0", parent=root)
    s0b = AnyNode(id="sub0B", parent=s0)
    s0a = AnyNode(id="sub0A", parent=s0)
    s1 = AnyNode(id="sub1", parent=root)
    s1a = AnyNode(id="sub1A", parent=s1)
    s1b = AnyNode(id="sub1B", parent=s1)
    s1c = AnyNode(id="sub1C", parent=s1)
    s1ca = AnyNode(id="sub1Ca", parent=s1c)

    lines = [
        '{',
        '  "children": [',
        '    {',
        '      "children": [',
        '        {',
        '          "id": "sub0B"',
        '        },',
        '        {',
        '          "id": "sub0A"',
        '        }',
        '      ],',
        '      "id": "sub0"',
        '    },',
        '    {',
        '      "children": [',
        '        {',
        '          "id": "sub1A"',
        '        },',
        '        {',
        '          "id": "sub1B"',
        '        },',
        '        {',
        '          "children": [',
        '            {',
        '              "id": "sub1Ca"',
        '            }',
        '          ],',
        '          "id": "sub1C"',
        '        }',
        '      ],',
        '      "id": "sub1"',
        '    }',
        '  ],',
        '  "id": "root"',
        '}'
    ]

    exporter = JsonExporter(indent=2, sort_keys=True)
    eq_(exporter.export(root), "\n".join(lines))
    with TemporaryDirectory() as tmpdirname:
        genfile = tmpdirname + os.sep + "gen.txt"
        reffile = tmpdirname + os.sep + "ref.txt"
        with open(genfile, "w") as gen:
            exporter.write(root, gen)
            with open(reffile, "w") as ref:
                ref.write("\n".join(lines))
        assert filecmp.cmp(reffile, genfile)
