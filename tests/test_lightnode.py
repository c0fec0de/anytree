from anytree import LightNodeMixin, LoopError, PostOrderIter, PreOrderIter, TreeError

from .helper import assert_raises


class LightNode(LightNodeMixin):
    __slots__ = ["name"]

    def __init__(self, name, parent=None, children=None):
        self.name = name
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        path = self.separator.join([""] + [str(node.name) for node in self.path])
        return f"{self.__class__.__name__}({path!r})"


def test_parent_child():
    """A tree parent and child attributes."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1a = LightNode("sub1A", parent=s1)
    s1b = LightNode("sub1B", parent=s1)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.parent is None
    assert root.children == (s0, s1)
    assert s0.parent == root
    assert s0.children == (s0b, s0a)
    assert s0b.parent == s0
    assert s0b.children == ()
    assert s0a.parent == s0
    assert s0a.children == ()
    assert s1.parent == root
    assert s1.children == (s1a, s1b, s1c)
    assert s1a.parent == s1
    assert s1a.children == ()
    assert s1b.parent == s1
    assert s1b.children == ()
    assert s1c.parent == s1
    assert s1c.children == (s1ca,)
    assert s1ca.parent == s1c
    assert s1ca.children == ()

    # change parent
    s1ca.parent = s0

    assert root.parent is None
    assert root.children == (s0, s1)
    assert s0.parent == root
    assert s0.children == (s0b, s0a, s1ca)
    assert s0b.parent == s0
    assert s0b.children == ()
    assert s0a.parent == s0
    assert s0a.children == ()
    assert s1.parent == root
    assert s1.children == (s1a, s1b, s1c)
    assert s1a.parent == s1
    assert s1a.children == ()
    assert s1b.parent == s1
    assert s1b.children == ()
    assert s1c.parent == s1
    assert s1c.children == ()
    assert s1ca.parent == s0
    assert s1ca.children == ()

    # break tree into two
    s1.parent = None

    assert root.parent is None
    assert root.children == (s0,)
    assert s0.parent == root
    assert s0.children == (s0b, s0a, s1ca)
    assert s0b.parent == s0
    assert s0b.children == ()
    assert s0a.parent == s0
    assert s0a.children == ()
    assert s1.parent is None
    assert s1.children == (s1a, s1b, s1c)
    assert s1a.parent == s1
    assert s1a.children == ()
    assert s1b.parent == s1
    assert s1b.children == ()
    assert s1c.parent == s1
    assert s1c.children == ()
    assert s1ca.parent == s0
    assert s1ca.children == ()

    # set to the same
    s1b.parent = s1

    assert root.parent is None
    assert root.children == (s0,)
    assert s0.parent == root
    assert s0.children == (s0b, s0a, s1ca)
    assert s0b.parent == s0
    assert s0b.children == ()
    assert s0a.parent == s0
    assert s0a.children == ()
    assert s1.parent is None
    assert s1.children == (s1a, s1b, s1c)
    assert s1a.parent == s1
    assert s1a.children == ()
    assert s1b.parent == s1
    assert s1b.children == ()
    assert s1c.parent == s1
    assert s1c.children == ()
    assert s1ca.parent == s0
    assert s1ca.children == ()


def test_detach_children():
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1a = LightNode("sub1A", parent=s1)
    s1b = LightNode("sub1B", parent=s1)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.descendants == (s0, s0b, s0a, s1, s1a, s1b, s1c, s1ca)
    del s0.children
    assert root.descendants == (s0, s1, s1a, s1b, s1c, s1ca)
    del s1.children
    assert root.descendants == (s0, s1)


def test_children_setter():
    root = LightNode("root")
    s0 = LightNode("sub0")
    s1 = LightNode("sub0A")
    s0a = LightNode("sub0B")

    root.children = [s0, s1]
    s0.children = [s0a]
    assert root.descendants == (s0, s0a, s1)

    with assert_raises(LoopError, "Cannot set parent. LightNode('/root/sub0') cannot be parent of itself."):
        s0.children = [s0]

    # test whether tree is unchanged after LoopError
    assert root.descendants == (s0, s0a, s1)

    with assert_raises(
        LoopError, "Cannot set parent. LightNode('/root/sub0') is parent of LightNode('/root/sub0/sub0B')."
    ):
        s0a.children = [s0]

    # test whether tree is unchanged after LoopError
    assert root.descendants == (s0, s0a, s1)

    root.children = [s0, s1]
    s0.children = [s0a]
    s0a.children = [s1]
    assert root.descendants == (s0, s0a, s1)


def test_children_setter_large():
    root = LightNode("root")
    s0 = LightNode("sub0")
    s0b = LightNode("sub0B")
    s0a = LightNode("sub0A")
    s1 = LightNode("sub1")
    s1a = LightNode("sub1A")
    s1b = LightNode("sub1B")
    s1c = LightNode("sub1C")
    s1ca = LightNode("sub1Ca")

    root.children = [s0, s1]
    assert root.descendants == (s0, s1)
    s0.children = [s0a, s0b]
    assert root.descendants == (s0, s0a, s0b, s1)
    s1.children = [s1a, s1b, s1c]
    assert root.descendants == (s0, s0a, s0b, s1, s1a, s1b, s1c)
    with assert_raises(TypeError, "'LightNode' object is not iterable"):
        s1.children = s1ca
    assert root.descendants == (s0, s0a, s0b, s1, s1a, s1b, s1c)


def test_node_children_multiple():
    root = LightNode("root")
    sub = LightNode("sub")
    with assert_raises(TreeError, "Cannot add node LightNode('/sub') multiple times as child."):
        root.children = [sub, sub]


def test_recursion_detection():
    """Recursion detection."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)

    # try recursion
    assert root.parent is None
    try:
        root.parent = root
    except LoopError as exc:
        assert str(exc) == "Cannot set parent. LightNode('/root') cannot be parent of itself."
        assert root.parent is None
    else:
        raise AssertionError

    assert root.parent is None
    try:
        root.parent = s0a
    except LoopError as exc:
        assert str(exc) == ("Cannot set parent. LightNode('/root') is parent of LightNode('/root/sub0/sub0A').")
        assert root.parent is None
    else:
        raise AssertionError

    assert s0.parent is root
    try:
        s0.parent = s0a
    except LoopError as exc:
        assert str(exc) == ("Cannot set parent. LightNode('/root/sub0') is parent of LightNode('/root/sub0/sub0A').")
        assert s0.parent is root
    else:
        raise AssertionError


def test_ancestors():
    """Node.ancestors."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.ancestors == ()
    assert s0.ancestors == (root,)
    assert s0b.ancestors == (root, s0)
    assert s0a.ancestors == (root, s0)
    assert s1ca.ancestors == (root, s1, s1c)


def test_node_children_init():
    """Node With Children Attribute."""
    root = LightNode("root", children=[LightNode("a", children=[LightNode("aa")]), LightNode("b")])
    assert repr(root.descendants) == "(LightNode('/root/a'), LightNode('/root/a/aa'), LightNode('/root/b'))"


def test_descendants():
    """Node.descendants."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.descendants == (s0, s0b, s0a, s1, s1c, s1ca)
    assert s1.descendants == (s1c, s1ca)
    assert s1c.descendants == (s1ca,)
    assert s1ca.descendants == ()


def test_root():
    """Node.root."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.root == root
    assert s0.root == root
    assert s0b.root == root
    assert s0a.root == root
    assert s1.root == root
    assert s1c.root == root
    assert s1ca.root == root


def test_siblings():
    """Node.siblings."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.siblings == ()
    assert s0.siblings == (s1,)
    assert s0b.siblings == (s0a,)
    assert s0a.siblings == (s0b,)
    assert s1.siblings == (s0,)
    assert s1c.siblings == ()
    assert s1ca.siblings == ()


def test_is_leaf():
    """Node.is_leaf."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.is_leaf is False
    assert s0.is_leaf is False
    assert s0b.is_leaf is True
    assert s0a.is_leaf is True
    assert s1.is_leaf is False
    assert s1c.is_leaf is False
    assert s1ca.is_leaf is True


def test_leaves():
    """Node.leaves."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.leaves == (s0b, s0a, s1ca)
    assert s0.leaves == (s0b, s0a)
    assert s0b.leaves == (s0b,)
    assert s0a.leaves == (s0a,)
    assert s1.leaves == (s1ca,)
    assert s1c.leaves == (s1ca,)
    assert s1ca.leaves == (s1ca,)


def test_is_root():
    """Node.is_root."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.is_root is True
    assert s0.is_root is False
    assert s0b.is_root is False
    assert s0a.is_root is False
    assert s1.is_root is False
    assert s1c.is_root is False
    assert s1ca.is_root is False


def test_height():
    """Node.height."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.height == 3
    assert s0.height == 1
    assert s0b.height == 0
    assert s0a.height == 0
    assert s1.height == 2
    assert s1c.height == 1
    assert s1ca.height == 0


def test_size():
    """Node.size."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.size == 7
    assert s0.size == 3
    assert s0b.size == 1
    assert s0a.size == 1
    assert s1.size == 3
    assert s1c.size == 2
    assert s1ca.size == 1


def test_depth():
    """Node.depth."""
    root = LightNode("root")
    s0 = LightNode("sub0", parent=root)
    s0b = LightNode("sub0B", parent=s0)
    s0a = LightNode("sub0A", parent=s0)
    s1 = LightNode("sub1", parent=root)
    s1c = LightNode("sub1C", parent=s1)
    s1ca = LightNode("sub1Ca", parent=s1c)

    assert root.depth == 0
    assert s0.depth == 1
    assert s0b.depth == 2
    assert s0a.depth == 2
    assert s1.depth == 1
    assert s1c.depth == 2
    assert s1ca.depth == 3


def test_parent():
    """Parent attribute."""
    foo = LightNodeMixin()
    assert foo.parent is None


def test_pre_order_iter():
    """Pre-Order Iterator."""
    f = LightNode("f")
    b = LightNode("b", parent=f)
    a = LightNode("a", parent=b)
    d = LightNode("d", parent=b)
    c = LightNode("c", parent=d)
    e = LightNode("e", parent=d)
    g = LightNode("g", parent=f)
    i = LightNode("i", parent=g)
    h = LightNode("h", parent=i)

    assert [node.name for node in PreOrderIter(f)] == ["f", "b", "a", "d", "c", "e", "g", "i", "h"]


def test_post_order_iter():
    """Post-Order Iterator."""
    f = LightNode("f")
    b = LightNode("b", parent=f)
    a = LightNode("a", parent=b)
    d = LightNode("d", parent=b)
    c = LightNode("c", parent=d)
    e = LightNode("e", parent=d)
    g = LightNode("g", parent=f)
    i = LightNode("i", parent=g)
    h = LightNode("h", parent=i)

    assert [node.name for node in PostOrderIter(f)] == ["a", "c", "e", "d", "b", "h", "i", "g", "f"]


def test_hookups():
    """Hookup attributes #29."""

    class MyLightNode(LightNode):
        def _pre_attach(self, parent):
            assert str(self.parent) == "None"
            assert self.children == ()
            assert str(self.path) == "(MyLightNode('/B'),)"

        def _post_attach(self, parent):
            assert str(self.parent) == "MyLightNode('/A')"
            assert self.children == ()
            assert str(self.path) == "(MyLightNode('/A'), MyLightNode('/A/B'))"

        def _pre_detach(self, parent):
            assert str(self.parent) == "MyLightNode('/A')"
            assert self.children == ()
            assert str(self.path) == "(MyLightNode('/A'), MyLightNode('/A/B'))"

        def _post_detach(self, parent):
            assert str(self.parent) == "None"
            assert self.children == ()
            assert str(self.path) == "(MyLightNode('/B'),)"

    node_a = MyLightNode("A")
    node_b = MyLightNode("B", node_a)  # attach B on A
    node_b.parent = None  # detach B from A
