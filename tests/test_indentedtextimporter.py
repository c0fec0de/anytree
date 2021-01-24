# -*- coding: utf-8 -*-
from nose.tools import eq_

from anytree import Node
from anytree import RenderTree
from anytree.importer import IndentedTextImporter, IndentedTextImporterError
from helper import eq_str


docstring_sample = """
sub0
  sub0A
  sub0B
sub1
"""[1:-1]

docstring_sample_expected = """
Node('/root')
├── Node('/root/sub0')
│   ├── Node('/root/sub0/sub0A')
│   └── Node('/root/sub0/sub0B')
└── Node('/root/sub1')
"""[1:-1]

faulty_indent = """
sub0
  sub0A
   sub0B
sub1
"""[1:-1]

early_bad_indent = """
        
   sub0 - (note: only whitespace in line above)
   sub1
"""[1:-1]

large_example = """
foo
  bar
    baz
  this line has a lot of text on it
    so does this one; lots of text to go around here
  what if I embed a / in here
    these/should/still/work/
      even/though/we're/filling/them/with////slashes//

and there was a blank line in here too,
                     
  including blank lines with white space,
  and indentation afterwards
how is it?
"""[1:-1]

large_example_expected = """
Node('/root')
├── Node('/root/foo')
│   ├── Node('/root/foo/bar')
│   │   └── Node('/root/foo/bar/baz')
│   ├── Node('/root/foo/this line has a lot of text on it')
│   │   └── Node('/root/foo/this line has a lot of text on it/so does this one; lots of text to go around here')
│   └── Node('/root/foo/what if I embed a / in here')
│       └── Node('/root/foo/what if I embed a / in here/these/should/still/work/')
│           └── Node("/root/foo/what if I embed a / in here/these/should/still/work//even/though/we're/filling/them/with////slashes//")
├── Node('/root/and there was a blank line in here too,')
│   ├── Node('/root/and there was a blank line in here too,/including blank lines with white space,')
│   └── Node('/root/and there was a blank line in here too,/and indentation afterwards')
└── Node('/root/how is it?')
"""[1:-1]


def test_importer():
    """IndentedTextImporter test"""
    importer = IndentedTextImporter()
    root = importer.import_(docstring_sample)
    r = RenderTree(root)
    eq_str(str(r), docstring_sample_expected)


def test_faulty_indent():
    """IndentedTextImporter: bad indentation test"""
    importer = IndentedTextImporter()
    try:
        root = importer.import_(faulty_indent)
    except IndentedTextImporterError as e:
        (err_name, err_lineno) = e.args
        if err_name == "bad indent at line" and err_lineno == 2:
            pass
        else:
            raise ValueError("expected bad indent error on line 2")


def test_early_bad_indent():
    """IndentedTextImporter: bad indentation test"""
    importer = IndentedTextImporter()
    try:
        root = importer.import_(early_bad_indent)
    except IndentedTextImporterError as e:
        (err_name, err_lineno) = e.args
        if err_name == "bad indent at line" and err_lineno == 1:
            pass
        else:
            raise ValueError("expected bad indent error on line 1")


def test_large_example():
    """IndentedTextImporter: bad indentation test"""
    importer = IndentedTextImporter()
    root = importer.import_(large_example)
    r = RenderTree(root)
    eq_str(str(r), large_example_expected)


