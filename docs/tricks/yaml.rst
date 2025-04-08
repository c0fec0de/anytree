YAML Import/Export
==================

YAML_ (YAML Ain't Markup Language) is a human-readable data serialization language.

PYYAML_ implements importer and exporter in python. *Please install it, before continuing*

.. note::

    anytree package does not depend on any external packages.
    It does **NOT** include PYYAML_.

.. Warning::

    It is not safe to call yaml.load with any data received from an untrusted source! yaml.load is as powerful as pickle.load and so may call any Python function.
    The yaml.safe_load function limits the load functionality to built-in types.

Export
------

The :any:`DictExporter` converts any tree to a dictionary, which can be handled
by `yaml.dump`.

>>> import yaml
>>> from anytree import AnyNode
>>> from anytree.exporter import DictExporter

Example tree:

>>> root = AnyNode(a="root")
>>> s0 = AnyNode(a="sub0", parent=root)
>>> s0a = AnyNode(a="sub0A", b="foo", parent=s0)
>>> s0b = AnyNode(a="sub0B", parent=s0)
>>> s1 = AnyNode(a="sub1", parent=root)

Export to dictionary and convert to YAML:

>>> dct = DictExporter().export(root)
>>> print(yaml.dump(dct, default_flow_style=False))
a: root
children:
- a: sub0
  children:
  - a: sub0A
    b: foo
  - a: sub0B
- a: sub1
<BLANKLINE>

:any:`DictExporter` controls the content.
`yaml.dump` controls the YAML related stuff.

To dump to a file, use an file object as second argument:

>>> with open("/path/to/file", "w") as file:  # doctest: +SKIP
...     yaml.dump(data, file)

Import
------

The `yaml.load` function reads YAML data --- a dictionary, which
:any:`DictImporter` converts to a tree.

>>> import yaml
>>> from anytree.importer import DictImporter
>>> from pprint import pprint  # just for nice printing
>>> from anytree import RenderTree  # just for nice printing

Example data:

>>> data = """
... a: root
... children:
... - a: sub0
...   children:
...   - a: sub0A
...     b: foo
...   - a: sub0B
... - a: sub1
... """

Import to dictionary and convert to tree:

>>> dct = yaml.load(data, Loader=yaml.Loader)
>>> pprint(dct)
{'a': 'root',
 'children': [{'a': 'sub0',
               'children': [{'a': 'sub0A', 'b': 'foo'}, {'a': 'sub0B'}]},
              {'a': 'sub1'}]}
>>> root = DictImporter().import_(dct)
>>> print(RenderTree(root))
AnyNode(a='root')
├── AnyNode(a='sub0')
│   ├── AnyNode(a='sub0A', b='foo')
│   └── AnyNode(a='sub0B')
└── AnyNode(a='sub1')

.. _YAML: https://en.wikipedia.org/wiki/YAML

.. _PYYAML: http://pyyaml.org/wiki/PyYAMLDocumentation
