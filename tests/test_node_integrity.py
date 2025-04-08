from anytree import Node

from .helper import assert_raises, eq_


def test_readonly_pre():
    """Read Only Use case, where Exceptions in _pre_{attach,detach} avoid modifications."""

    class ReadonlyError(RuntimeError):
        pass

    class ReadonlyNode(Node):
        _is_readonly = False

        def _pre_attach(self, parent):
            if self._is_readonly:
                raise ReadonlyError

        def _pre_detach(self, parent):
            if self._is_readonly:
                raise ReadonlyError

    # construct and make readonly!
    root = ReadonlyNode("root")
    s0 = ReadonlyNode("sub0", parent=root)
    s0b = ReadonlyNode("sub0B", parent=s0)
    s0a = ReadonlyNode("sub0A", parent=s0)
    s1 = ReadonlyNode("sub1", parent=root)
    s1a = ReadonlyNode("sub1A", parent=s1)
    s1b = ReadonlyNode("sub1B", parent=s1)
    s1c = ReadonlyNode("sub1C", parent=s1)
    s1ca = ReadonlyNode("sub1Ca", parent=s1c)
    ReadonlyNode._is_readonly = True

    def check():
        eq_(root.parent, None)
        eq_(root.children, (s0, s1))
        eq_(s0.parent, root)
        eq_(s0.children, (s0b, s0a))
        eq_(s0b.parent, s0)
        eq_(s0b.children, ())
        eq_(s0a.parent, s0)
        eq_(s0a.children, ())
        eq_(s1.parent, root)
        eq_(s1.children, (s1a, s1b, s1c))
        eq_(s1a.parent, s1)
        eq_(s1a.children, ())
        eq_(s1b.parent, s1)
        eq_(s1b.children, ())
        eq_(s1c.parent, s1)
        eq_(s1c.children, (s1ca,))
        eq_(s1ca.parent, s1c)
        eq_(s1ca.children, ())

    check()
    with assert_raises(ReadonlyError, ""):
        s1ca.parent = s0
    check()
    with assert_raises(ReadonlyError, ""):
        s1ca.parent = None
    check()
    with assert_raises(ReadonlyError, ""):
        s0.children = []
    check()
