from anytree import AnyNode, LoopError, Node, NodeMixin, PostOrderIter, PreOrderIter, TreeError

from .helper import assert_raises


def test_node_parent_error():
    """Node Parent Error."""
    with assert_raises(TreeError, "Parent node 'parent' is not of type 'NodeMixin'."):
        Node("root", "parent")


def test_parent_child():
    """A tree parent and child attributes."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1a = Node("sub1A", parent=s1)
    s1b = Node("sub1B", parent=s1)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

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
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1a = Node("sub1A", parent=s1)
    s1b = Node("sub1B", parent=s1)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.descendants == (s0, s0b, s0a, s1, s1a, s1b, s1c, s1ca)
    del s0.children
    assert root.descendants == (s0, s1, s1a, s1b, s1c, s1ca)
    del s1.children
    assert root.descendants == (s0, s1)


def test_children_setter():
    root = Node("root")
    s0 = Node("sub0")
    s1 = Node("sub0A")
    s0a = Node("sub0B")

    root.children = [s0, s1]
    s0.children = [s0a]
    assert root.descendants == (s0, s0a, s1)

    with assert_raises(LoopError, "Cannot set parent. Node('/root/sub0') cannot be parent of itself."):
        s0.children = [s0]

    # test whether tree is unchanged after LoopError
    assert root.descendants == (s0, s0a, s1)

    with assert_raises(LoopError, "Cannot set parent. Node('/root/sub0') is parent of Node('/root/sub0/sub0B')."):
        s0a.children = [s0]

    # test whether tree is unchanged after LoopError
    assert root.descendants == (s0, s0a, s1)

    root.children = [s0, s1]
    s0.children = [s0a]
    s0a.children = [s1]
    assert root.descendants == (s0, s0a, s1)


def test_children_setter_large():
    root = Node("root")
    s0 = Node("sub0")
    s0b = Node("sub0B")
    s0a = Node("sub0A")
    s1 = Node("sub1")
    s1a = Node("sub1A")
    s1b = Node("sub1B")
    s1c = Node("sub1C")
    s1ca = Node("sub1Ca")

    root.children = [s0, s1]
    assert root.descendants == (s0, s1)
    s0.children = [s0a, s0b]
    assert root.descendants == (s0, s0a, s0b, s1)
    s1.children = [s1a, s1b, s1c]
    assert root.descendants == (s0, s0a, s0b, s1, s1a, s1b, s1c)
    with assert_raises(TypeError, "'Node' object is not iterable"):
        s1.children = s1ca
    assert root.descendants == (s0, s0a, s0b, s1, s1a, s1b, s1c)


def test_node_children_type():
    root = Node("root")
    with assert_raises(TreeError, "Cannot add non-node object 'string'. It is not a subclass of 'NodeMixin'."):
        root.children = ["string"]


def test_node_children_multiple():
    root = Node("root")
    sub = Node("sub")
    with assert_raises(TreeError, "Cannot add node Node('/sub') multiple times as child."):
        root.children = [sub, sub]


def test_recursion_detection():
    """Recursion detection."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)

    # try recursion
    assert root.parent is None
    try:
        root.parent = root
    except LoopError as exc:
        assert str(exc) == "Cannot set parent. Node('/root') cannot be parent of itself."
        assert root.parent is None
    else:
        raise AssertionError

    assert root.parent is None
    try:
        root.parent = s0a
    except LoopError as exc:
        assert str(exc) == ("Cannot set parent. Node('/root') is parent of Node('/root/sub0/sub0A').")
        assert root.parent is None
    else:
        raise AssertionError

    assert s0.parent is root
    try:
        s0.parent = s0a
    except LoopError as exc:
        assert str(exc) == ("Cannot set parent. Node('/root/sub0') is parent of Node('/root/sub0/sub0A').")
        assert s0.parent is root
    else:
        raise AssertionError


def test_repr():
    """Node representation."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s1 = Node("sub1", parent=root, foo=42, bar="c0fe")

    assert repr(root) == "Node('/root')"
    assert repr(s0) == "Node('/root/sub0')"
    assert repr(s1) == "Node('/root/sub1', bar='c0fe', foo=42)"


def test_ancestors():
    """Node.ancestors."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.ancestors == ()
    assert s0.ancestors == (root,)
    assert s0b.ancestors == (root, s0)
    assert s0a.ancestors == (root, s0)
    assert s1ca.ancestors == (root, s1, s1c)
    # deprecated typo
    assert s1ca.ancestors == (root, s1, s1c)


def test_node_children_init():
    """Node With Children Attribute."""
    root = Node("root", children=[Node("a", children=[Node("aa")]), Node("b")])
    assert repr(root.descendants) == "(Node('/root/a'), Node('/root/a/aa'), Node('/root/b'))"


def test_anynode_children_init():
    """Anynode With Children Attribute."""
    root = AnyNode(foo="root", children=[AnyNode(foo="a", children=[AnyNode(foo="aa")]), AnyNode(foo="b")])
    assert repr(root.descendants) == "(AnyNode(foo='a'), AnyNode(foo='aa'), AnyNode(foo='b'))"


def test_descendants():
    """Node.descendants."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.descendants == (s0, s0b, s0a, s1, s1c, s1ca)
    assert s1.descendants == (s1c, s1ca)
    assert s1c.descendants == (s1ca,)
    assert s1ca.descendants == ()


def test_root():
    """Node.root."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.root == root
    assert s0.root == root
    assert s0b.root == root
    assert s0a.root == root
    assert s1.root == root
    assert s1c.root == root
    assert s1ca.root == root


def test_siblings():
    """Node.siblings."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.siblings == ()
    assert s0.siblings == (s1,)
    assert s0b.siblings == (s0a,)
    assert s0a.siblings == (s0b,)
    assert s1.siblings == (s0,)
    assert s1c.siblings == ()
    assert s1ca.siblings == ()


def test_is_leaf():
    """Node.is_leaf."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.is_leaf is False
    assert s0.is_leaf is False
    assert s0b.is_leaf is True
    assert s0a.is_leaf is True
    assert s1.is_leaf is False
    assert s1c.is_leaf is False
    assert s1ca.is_leaf is True


def test_leaves():
    """Node.leaves."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.leaves == (s0b, s0a, s1ca)
    assert s0.leaves == (s0b, s0a)
    assert s0b.leaves == (s0b,)
    assert s0a.leaves == (s0a,)
    assert s1.leaves == (s1ca,)
    assert s1c.leaves == (s1ca,)
    assert s1ca.leaves == (s1ca,)


def test_is_root():
    """Node.is_root."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.is_root is True
    assert s0.is_root is False
    assert s0b.is_root is False
    assert s0a.is_root is False
    assert s1.is_root is False
    assert s1c.is_root is False
    assert s1ca.is_root is False


def test_height():
    """Node.height."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.height == 3
    assert s0.height == 1
    assert s0b.height == 0
    assert s0a.height == 0
    assert s1.height == 2
    assert s1c.height == 1
    assert s1ca.height == 0


def test_size():
    """Node.size."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.size == 7
    assert s0.size == 3
    assert s0b.size == 1
    assert s0a.size == 1
    assert s1.size == 3
    assert s1c.size == 2
    assert s1ca.size == 1


def test_depth():
    """Node.depth."""
    root = Node("root")
    s0 = Node("sub0", parent=root)
    s0b = Node("sub0B", parent=s0)
    s0a = Node("sub0A", parent=s0)
    s1 = Node("sub1", parent=root)
    s1c = Node("sub1C", parent=s1)
    s1ca = Node("sub1Ca", parent=s1c)

    assert root.depth == 0
    assert s0.depth == 1
    assert s0b.depth == 2
    assert s0a.depth == 2
    assert s1.depth == 1
    assert s1c.depth == 2
    assert s1ca.depth == 3


def test_parent():
    """Parent attribute."""
    foo = NodeMixin()
    assert foo.parent is None


def test_pre_order_iter():
    """Pre-Order Iterator."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)

    assert [node.name for node in PreOrderIter(f)] == ["f", "b", "a", "d", "c", "e", "g", "i", "h"]


def test_post_order_iter():
    """Post-Order Iterator."""
    f = Node("f")
    b = Node("b", parent=f)
    a = Node("a", parent=b)
    d = Node("d", parent=b)
    c = Node("c", parent=d)
    e = Node("e", parent=d)
    g = Node("g", parent=f)
    i = Node("i", parent=g)
    h = Node("h", parent=i)

    assert [node.name for node in PostOrderIter(f)] == ["a", "c", "e", "d", "b", "h", "i", "g", "f"]


def test_anyname():
    """Support any type as name."""
    myroot = Node([1, 2, 3])
    Node("/foo", parent=myroot)
    assert str(myroot) == "Node('/[1, 2, 3]')"


def test_node_kwargs():
    """Ticket #24."""

    class MyNode(Node):
        def __init__(self, name, parent=None, **kwargs):
            super().__init__(name, parent, **kwargs)

        def _post_attach(self, parent):
            print(self.my_attribute)

    node_a = MyNode("A")
    node_b = MyNode("B", node_a, my_attribute=True)
    assert repr(node_b) == "MyNode('/A/B', my_attribute=True)"


def test_hookups():
    """Hookup attributes #29."""

    class MyNode(Node):
        def _pre_attach(self, parent):
            assert str(self.parent) == "None"
            assert self.children == ()
            assert str(self.path) == "(MyNode('/B'),)"

        def _post_attach(self, parent):
            assert str(self.parent) == "MyNode('/A')"
            assert self.children == ()
            assert str(self.path) == "(MyNode('/A'), MyNode('/A/B'))"

        def _pre_detach(self, parent):
            assert str(self.parent) == "MyNode('/A')"
            assert self.children == ()
            assert str(self.path) == "(MyNode('/A'), MyNode('/A/B'))"

        def _post_detach(self, parent):
            assert str(self.parent) == "None"
            assert self.children == ()
            assert str(self.path) == "(MyNode('/B'),)"

    node_a = MyNode("A")
    node_b = MyNode("B", node_a)  # attach B on A
    node_b.parent = None  # detach B from A


def test_any_node_parent_error():
    """Any Node Parent Error."""
    with assert_raises(TreeError, "Parent node 'r' is not of type 'NodeMixin'."):
        AnyNode("r")


def test_any_node():
    """Any Node."""
    r = AnyNode()
    a = AnyNode()
    b = AnyNode(foo=4)
    assert r.parent is None
    assert a.parent is None
    assert b.parent is None
    a.parent = r
    b.parent = r
    assert r.children == (a, b)
    assert repr(r) == "AnyNode()"
    assert repr(a) == "AnyNode()"
    assert repr(b) == "AnyNode(foo=4)"


def test_eq_overwrite():
    """Node with overwritten __eq__."""

    class EqOverwrittingNode(NodeMixin):
        def __init__(self, a, b, parent=None):
            super().__init__()
            self.a = a
            self.b = b
            self.parent = parent

        def __eq__(self, other):
            if isinstance(other, EqOverwrittingNode):
                return self.a == other.a and self.b == other.b
            return NotImplemented

    r = EqOverwrittingNode(0, 0)
    a = EqOverwrittingNode(1, 0, parent=r)
    b = EqOverwrittingNode(1, 0, parent=r)
    assert a.parent is r
    assert b.parent is r
    assert a.a == 1
    assert a.b == 0
    assert b.a == 1
    assert b.b == 0


def test_tuple():
    """Tuple as parent."""
    with assert_raises(TreeError, "Parent node (1, 0, 3) is not of type 'NodeMixin'."):
        Node((0, 1, 2), parent=(1, 0, 3))


def test_tuple_as_children():
    """Tuple as children."""
    n = Node("foo")
    with assert_raises(TreeError, "Cannot add non-node object (0, 1, 2). It is not a subclass of 'NodeMixin'."):
        n.children = [(0, 1, 2)]
