import filecmp
import os
from tempfile import NamedTemporaryFile

from anytree import AnyNode
from anytree.exporter import JsonExporter

from .helper import eq_


def test_json_exporter():
    """Json Exporter."""
    root = AnyNode(id="root")
    s0 = AnyNode(id="sub0", parent=root)
    AnyNode(id="sub0B", parent=s0)
    AnyNode(id="sub0A", parent=s0)
    s1 = AnyNode(id="sub1", parent=root)
    AnyNode(id="sub1A", parent=s1)
    AnyNode(id="sub1B", parent=s1)
    s1c = AnyNode(id="sub1C", parent=s1)
    AnyNode(id="sub1Ca", parent=s1c)

    exporter = JsonExporter(indent=2, sort_keys=True)
    exported = exporter.export(root).splitlines()
    exported = [e.rstrip() for e in exported]  # just a fix for a strange py2x behavior.
    lines = [
        "{",
        '  "children": [',
        "    {",
        '      "children": [',
        "        {",
        '          "id": "sub0B"',
        "        },",
        "        {",
        '          "id": "sub0A"',
        "        }",
        "      ],",
        '      "id": "sub0"',
        "    },",
        "    {",
        '      "children": [',
        "        {",
        '          "id": "sub1A"',
        "        },",
        "        {",
        '          "id": "sub1B"',
        "        },",
        "        {",
        '          "children": [',
        "            {",
        '              "id": "sub1Ca"',
        "            }",
        "          ],",
        '          "id": "sub1C"',
        "        }",
        "      ],",
        '      "id": "sub1"',
        "    }",
        "  ],",
        '  "id": "root"',
        "}",
    ]
    eq_(exported, lines)

    exporter = JsonExporter(indent=2, sort_keys=True, maxlevel=2)
    exported = exporter.export(root).splitlines()
    exported = [e.rstrip() for e in exported]  # just a fix for a strange py2x behavior.
    limitedlines = [
        "{",
        '  "children": [',
        "    {",
        '      "id": "sub0"',
        "    },",
        "    {",
        '      "id": "sub1"',
        "    }",
        "  ],",
        '  "id": "root"',
        "}",
    ]

    eq_(exported, limitedlines)

    try:
        with NamedTemporaryFile(mode="w+", delete=False) as ref:
            with NamedTemporaryFile(mode="w+", delete=False) as gen:
                ref.write("\n".join(lines))
                exporter.write(root, gen)
        # on Windows, you must close the files before comparison
        filecmp.cmp(ref.name, gen.name)
    finally:
        os.remove(ref.name)
        os.remove(gen.name)
