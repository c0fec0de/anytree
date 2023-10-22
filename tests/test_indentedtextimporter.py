# -*- coding: utf-8 -*-
from anytree.importer import IndentedTextImporter
from anytree.importer import IndentedTextImporterError

docstring_sample = """
sub0
  sub0A
  sub0B
sub1
"""[1:-1]

check_docstring_sample = ["root", 0, "sub0", 0, "sub0A", -1, 1, "sub0B", -1, -1,
                          1, "sub1"]


faulty_indent = """
sub0
  sub0A
   sub0B
sub1
"""[1:-1]


early_bad_indent = """
   sub0
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
      /with/many////slashes

and there was a blank line in here too,

  and another blank line,
  and indentation afterwards
how is it?
"""[1:-1]


check_large_example = ["root", 0, "foo", 0, "bar", 0, "baz", -1, -1, 1,
                       "this line has a lot of text on it", 0,
                       "so does this one; lots of text to go around here",
                       -1, -1, 2, "what if I embed a / in here", 0,
                       "these/should/still/work/", 0, "/with/many////slashes",
                       -1, -1, -1, -1, 1,
                       "and there was a blank line in here too,", 0,
                       "and another blank line,", -1, 1,
                       "and indentation afterwards", -1, -1, 2, "how is it?"]


def check(node, instructions):
    for cmd in instructions:
        if cmd == -1:  # "go up"
            node = node.parent
        elif isinstance(cmd, int):  # "go to numbered child"
            node = node.children[cmd]
        else:
            if cmd != node.name:  # "verify that this is the text"
                raise ValueError("unexpected value located", cmd, node.name)


def test_importer():
    """IndentedTextImporter test"""
    importer = IndentedTextImporter()
    root = importer.import_(docstring_sample)
    check(root, check_docstring_sample)


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
        if err_name == "bad indent at line" and err_lineno == 0:
            pass
        else:
            raise ValueError("expected bad indent error on line 0")


def test_large_example():
    """IndentedTextImporter: bad indentation test"""
    importer = IndentedTextImporter()
    root = importer.import_(large_example)
    check(root, check_large_example)
