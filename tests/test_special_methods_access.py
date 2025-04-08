"""
The methods of the `NodeMixin` class should not access the user class special methods.

For instance, the user define a `MyNode` class as below:

```python
from anytree import NodeMixin


class MyNode(NodeMixin):
    def __init__(self, name, parent=None, children=None):
        super(MyNode, self).__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children
```

In this class, the used can implement some special methods, like ``__eq__`` or ``__len__``,
which can have a specific meaning not related to the Tree structure.
A good example could be a `NodeMixin` subclass which also implements `collections.abc.Mapping`:


```python
import collections

from anytree import NodeMixin


class MyMapping(NodeMixin, collections.abc.Mapping):
    def __init__(self, name, parent=None, children=None):
        super(MyMapping, self).__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children

    def __iter__(self):
        for child in self.children:
            yield child
            for item in child:
                yield item

    def __len__(self):
        return len(list(iter(self)))

    def __getitem__(self, name):
        for child in self:
            if child.name == name:
                return child
        raise KeyError(name)
```

In this example, the `NodeMixin` class shouldn't make any call to `__iter__`, `__len__` or `__getitem__`.

To avoid that, the `NodeMixin` class should respect the following rules:

- Do not compare nodes by value but by reference.
  In other words, the `NodeMixin` class should not use `==` or `!=` but compare nodes with the `id()` function.
  Comparison could be done with the `is` or `is not` operator. Avoid using `in` or `not in`.

- Do not use truth value testing to check if a node is "empty".
  The `NodeMixin` class should not `if node`, `if not node`, `while node` nor `while not node`.
  Instead, it must compare the node with `None` like this: `if node is not None`, `if node is None`,
  `while node is not None` or `while node is None`.

- Do not presume that nodes are hashable.
  The `NodeMixin` class should not store nodes in `set` or `dict`.
  Instead, it can store node IDs using the `id()` function.
"""

import functools
import unittest
from collections.abc import Mapping

from anytree import NodeMixin

# List of method names to which we want to control access:
#
# - This list does not contain the access control methods (`__getattribute__`, `__getattr__`,
#   `__setattr__`, and `__delattr__`) which are used by the NodeMixin class anyway.
# - This list does not contain `__new__`, `__init__`, and `__del__` which are required for testing.
# - Some methods are not available in all Python version: `__bytes__`, `__unicode__` and `__dir__`.

SPECIAL_METHODS = [
    # rich comparison methods
    "__lt__",
    "__le__",
    "__eq__",
    "__ne__",
    "__gt__",
    "__ge__",
    # repr/str/bytes
    "__repr__",
    "__str__",
    # "__bytes__",
    # "__unicode__",
    "__format__",
    # hashing
    "__hash__",
    # attribute listing
    # "__dir__",
    # pickle protocol
    "__getnewargs_ex__",
    "__getnewargs__",
    "__getstate__",
    "__setstate__",
    "__reduce_ex__",
    # object size
    "__sizeof__",
    # truth value testing
    "__bool__",
    # callable objects
    "__call__",
    # container types
    "__len__",
    "__length_hint__",
    "__getitem__",
    "__setitem__",
    "__delitem__",
    "__missing__",
    "__iter__",
    "__reversed__",
    "__contains__",
    # numeric types
    "__add__",
    "__sub__",
    "__mul__",
    "__matmul__",
    "__truediv__",
    "__floordiv__",
    "__mod__",
    "__divmod__",
    "__pow__",
    "__lshift__",
    "__rshift__",
    "__and__",
    "__xor__",
    "__or__",
    "__radd__",
    "__rsub__",
    "__rmul__",
    "__rmatmul__",
    "__rtruediv__",
    "__rfloordiv__",
    "__rmod__",
    "__rdivmod__",
    "__rpow__",
    "__rlshift__",
    "__rrshift__",
    "__rand__",
    "__rxor__",
    "__ror__",
    "__iadd__",
    "__isub__",
    "__imul__",
    "__imatmul__",
    "__itruediv__",
    "__ifloordiv__",
    "__imod__",
    "__ipow__",
    "__ilshift__",
    "__irshift__",
    "__iand__",
    "__ixor__",
    "__ior__",
    "__neg__",
    "__pos__",
    "__abs__",
    "__invert__",
    "__complex__",
    "__int__",
    "__float__",
    "__index__",
    "__round__",
    "__trunc__",
    "__floor__",
    "__ceil__",
    # With Statement Context Managers
    "__enter__",
    "__exit__",
]
SPECIAL_METHODS += [attr for attr in ["__bytes__", "__unicode__", "__dir"] if hasattr(object, attr)]


def prevent_access(attr, *args, **kwargs):
    raise AssertionError("invalid call to " + attr)


class MyNode(NodeMixin):
    @staticmethod
    def __new__(cls, *args, **kwargs):
        for attr in SPECIAL_METHODS:
            setattr(cls, attr, functools.partial(prevent_access, attr))
        return super(NodeMixin, cls).__new__(cls)

    def __init__(self, name, parent=None, children=None):
        super().__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children


class TestConsistency(unittest.TestCase):
    """Control the access to special methods."""

    def setUp(self):
        super().setUp()
        self.root1 = MyNode("root1")
        self.child1 = MyNode("child1", parent=self.root1)
        self.child2a = MyNode("child2a", parent=self.child1)
        self.child2b = MyNode("child2b", parent=self.child1)
        self.other = MyNode("other")

    def test_parent__root1(self):
        _ = self.root1.parent

    def test_parent__setter__root1(self):
        self.root1.parent = self.other

    def test_children__root1(self):
        _ = self.root1.children

    def test_children__setter__root1(self):
        self.root1.children = [self.other]

    def test_path__root1(self):
        _ = self.root1.path

    def test_iter_path_reverse__root1(self):
        for _ in self.root1.iter_path_reverse():
            pass

    def test_ancestors__root1(self):
        _ = self.root1.ancestors

    def test_descendants__root1(self):
        _ = self.root1.descendants

    def test_root__root1(self):
        _ = self.root1.root

    def test_siblings__root1(self):
        _ = self.root1.siblings

    def test_leaves__root1(self):
        _ = self.root1.leaves

    def test_is_leaf__root1(self):
        _ = self.root1.is_leaf

    def test_is_root__root1(self):
        _ = self.root1.is_root

    def test_height__root1(self):
        _ = self.root1.height

    def test_depth__root1(self):
        _ = self.root1.depth

    def test_parent__child2b(self):
        _ = self.child2b.parent

    def test_parent__setter__child2b(self):
        self.child2b.parent = self.other

    def test_children__child2b(self):
        _ = self.child2b.children

    def test_children__setter__child2b(self):
        self.child2b.children = [self.other]

    def test_path__child2b(self):
        _ = self.child2b.path

    def test_iter_path_reverse__child2b(self):
        for _ in self.child2b.iter_path_reverse():
            pass

    def test_ancestors__child2b(self):
        _ = self.child2b.ancestors

    def test_descendants__child2b(self):
        _ = self.child2b.descendants

    def test_root__child2b(self):
        _ = self.child2b.root

    def test_siblings__child2b(self):
        _ = self.child2b.siblings

    def test_leaves__child2b(self):
        _ = self.child2b.leaves

    def test_is_leaf__child2b(self):
        _ = self.child2b.is_leaf

    def test_is_root__child2b(self):
        _ = self.child2b.is_root

    def test_height__child2b(self):
        _ = self.child2b.height

    def test_depth__child2b(self):
        _ = self.child2b.depth


class MyMapping(NodeMixin, Mapping):
    """
    This class is used to demonstrate a possible implementation which defines some special methods.
    """

    def __init__(self, name, parent=None, children=None):
        super().__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children

    def __iter__(self):
        """Iterate over all children recursively."""
        for child in self.children:
            yield child
            yield from child

    def __len__(self):
        """Total number of children."""
        return len(list(iter(self)))

    def __getitem__(self, name):
        for child in self:
            if child.name == name:
                return child
        raise KeyError(name)


class TestMyMapping(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.root1 = MyMapping("root1")
        self.child1 = MyMapping("child1", parent=self.root1)
        self.child2a = MyMapping("child2a", parent=self.child1)
        self.child2b = MyMapping("child2b", parent=self.child1)

    def test_iter(self):
        expected_list = [self.child1, self.child2a, self.child2b]
        for actual, expected in zip(iter(self.root1), expected_list):
            self.assertIs(actual, expected)

    def test_len(self):
        self.assertEqual(len(self.root1), 3)

    def test_getitem(self):
        self.assertIs(self.root1["child1"], self.child1)
        self.assertIs(self.root1["child2a"], self.child2a)
        self.assertIs(self.root1["child2b"], self.child2b)
        with self.assertRaises(KeyError):
            _ = self.root1["missing"]
