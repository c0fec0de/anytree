from anytree import LoopError, Node

from .helper import assert_raises


class TNode(Node):
    TRACKING = []  # noqa: RUF012

    def _pre_detach(self, parent):
        """Method call before detaching from `parent`."""
        self.TRACKING.append(f"_pre_detach({self.name!r}, {parent.name!r})")

    def _post_detach(self, parent):
        """Method call after detaching from `parent`."""
        self.TRACKING.append(f"_post_detach({self.name!r}, {parent.name!r})")

    def _pre_attach(self, parent):
        """Method call before attaching to `parent`."""
        self.TRACKING.append(f"_pre_attach({self.name!r}, {parent.name!r})")

    def _post_attach(self, parent):
        """Method call after attaching to `parent`."""
        self.TRACKING.append(f"_post_attach({self.name!r}, {parent.name!r})")

    def _pre_detach_children(self, children):
        """Method call before detaching `children`."""
        self.TRACKING.append(f"_pre_detach_children({self.name!r}, {tuple(child.name for child in children)!r})")

    def _post_detach_children(self, children):
        """Method call after detaching `children`."""
        self.TRACKING.append(f"_post_detach_children({self.name!r}, {tuple(child.name for child in children)!r})")

    def _pre_attach_children(self, children):
        """Method call before attaching `children`."""
        self.TRACKING.append(f"_pre_attach_children({self.name!r}, {tuple(child.name for child in children)!r})")

    def _post_attach_children(self, children):
        """Method call after attaching `children`."""
        self.TRACKING.append(f"_post_attach_children({self.name!r}, {tuple(child.name for child in children)!r})")


def test_parent_child():
    """A tree parent and child attributes."""
    root = TNode("root")
    s0 = TNode("sub0", parent=root)
    s0b = TNode("sub0B", parent=s0)
    s0a = TNode("sub0A", parent=s0)
    s1 = TNode("sub1", parent=root)
    s1a = TNode("sub1A", parent=s1)
    s1b = TNode("sub1B", parent=s1)
    s1c = TNode("sub1C", parent=s1)
    s1ca = TNode("sub1Ca", parent=s1c)

    assert TNode.TRACKING == [
        "_pre_attach('sub0', 'root')",
        "_post_attach('sub0', 'root')",
        "_pre_attach('sub0B', 'sub0')",
        "_post_attach('sub0B', 'sub0')",
        "_pre_attach('sub0A', 'sub0')",
        "_post_attach('sub0A', 'sub0')",
        "_pre_attach('sub1', 'root')",
        "_post_attach('sub1', 'root')",
        "_pre_attach('sub1A', 'sub1')",
        "_post_attach('sub1A', 'sub1')",
        "_pre_attach('sub1B', 'sub1')",
        "_post_attach('sub1B', 'sub1')",
        "_pre_attach('sub1C', 'sub1')",
        "_post_attach('sub1C', 'sub1')",
        "_pre_attach('sub1Ca', 'sub1C')",
        "_post_attach('sub1Ca', 'sub1C')",
    ]
    TNode.TRACKING.clear()

    # change parent
    s1ca.parent = s0

    # break tree into two
    s1.parent = None

    # set to the same
    s1b.parent = s1

    assert TNode.TRACKING == [
        "_pre_detach('sub1Ca', 'sub1C')",
        "_post_detach('sub1Ca', 'sub1C')",
        "_pre_attach('sub1Ca', 'sub0')",
        "_post_attach('sub1Ca', 'sub0')",
        "_pre_detach('sub1', 'root')",
        "_post_detach('sub1', 'root')",
    ]
    TNode.TRACKING.clear()


def test_detach_children():
    root = TNode("root")
    s0 = TNode("sub0", parent=root)
    s0b = TNode("sub0B", parent=s0)
    s0a = TNode("sub0A", parent=s0)
    s1 = TNode("sub1", parent=root)
    s1a = TNode("sub1A", parent=s1)
    s1b = TNode("sub1B", parent=s1)
    s1c = TNode("sub1C", parent=s1)
    s1ca = TNode("sub1Ca", parent=s1c)

    assert TNode.TRACKING == [
        "_pre_attach('sub0', 'root')",
        "_post_attach('sub0', 'root')",
        "_pre_attach('sub0B', 'sub0')",
        "_post_attach('sub0B', 'sub0')",
        "_pre_attach('sub0A', 'sub0')",
        "_post_attach('sub0A', 'sub0')",
        "_pre_attach('sub1', 'root')",
        "_post_attach('sub1', 'root')",
        "_pre_attach('sub1A', 'sub1')",
        "_post_attach('sub1A', 'sub1')",
        "_pre_attach('sub1B', 'sub1')",
        "_post_attach('sub1B', 'sub1')",
        "_pre_attach('sub1C', 'sub1')",
        "_post_attach('sub1C', 'sub1')",
        "_pre_attach('sub1Ca', 'sub1C')",
        "_post_attach('sub1Ca', 'sub1C')",
    ]
    TNode.TRACKING.clear()

    del s0.children

    assert TNode.TRACKING == [
        "_pre_detach_children('sub0', ('sub0B', 'sub0A'))",
        "_pre_detach('sub0B', 'sub0')",
        "_post_detach('sub0B', 'sub0')",
        "_pre_detach('sub0A', 'sub0')",
        "_post_detach('sub0A', 'sub0')",
        "_post_detach_children('sub0', ('sub0B', 'sub0A'))",
    ]
    TNode.TRACKING.clear()

    del s1.children

    assert TNode.TRACKING == [
        "_pre_detach_children('sub1', ('sub1A', 'sub1B', 'sub1C'))",
        "_pre_detach('sub1A', 'sub1')",
        "_post_detach('sub1A', 'sub1')",
        "_pre_detach('sub1B', 'sub1')",
        "_post_detach('sub1B', 'sub1')",
        "_pre_detach('sub1C', 'sub1')",
        "_post_detach('sub1C', 'sub1')",
        "_post_detach_children('sub1', ('sub1A', 'sub1B', 'sub1C'))",
    ]
    TNode.TRACKING.clear()


def test_children_setter():
    root = TNode("root")
    s0 = TNode("sub0")
    s1 = TNode("sub0A")
    s0a = TNode("sub0B")

    assert TNode.TRACKING == []
    TNode.TRACKING.clear()

    root.children = [s0, s1]
    s0.children = [s0a]

    assert TNode.TRACKING == [
        "_pre_detach_children('root', ())",
        "_post_detach_children('root', ())",
        "_pre_attach_children('root', ('sub0', 'sub0A'))",
        "_pre_attach('sub0', 'root')",
        "_post_attach('sub0', 'root')",
        "_pre_attach('sub0A', 'root')",
        "_post_attach('sub0A', 'root')",
        "_post_attach_children('root', ('sub0', 'sub0A'))",
        "_pre_detach_children('sub0', ())",
        "_post_detach_children('sub0', ())",
        "_pre_attach_children('sub0', ('sub0B',))",
        "_pre_attach('sub0B', 'sub0')",
        "_post_attach('sub0B', 'sub0')",
        "_post_attach_children('sub0', ('sub0B',))",
    ]
    TNode.TRACKING.clear()

    with assert_raises(LoopError, "Cannot set parent. TNode('/root/sub0') cannot be parent of itself."):
        s0.children = [s0]

    # test whether tree is unchanged after LoopError
    assert TNode.TRACKING == [
        "_pre_detach_children('sub0', ('sub0B',))",
        "_pre_detach('sub0B', 'sub0')",
        "_post_detach('sub0B', 'sub0')",
        "_post_detach_children('sub0', ('sub0B',))",
        "_pre_attach_children('sub0', ('sub0',))",
        "_pre_detach_children('sub0', ())",
        "_post_detach_children('sub0', ())",
        "_pre_attach_children('sub0', ('sub0B',))",
        "_pre_attach('sub0B', 'sub0')",
        "_post_attach('sub0B', 'sub0')",
        "_post_attach_children('sub0', ('sub0B',))",
    ]
    TNode.TRACKING.clear()

    with assert_raises(LoopError, "Cannot set parent. TNode('/root/sub0') is parent of TNode('/root/sub0/sub0B')."):
        s0a.children = [s0]

    # test whether tree is unchanged after LoopError
    assert TNode.TRACKING == [
        "_pre_detach_children('sub0B', ())",
        "_post_detach_children('sub0B', ())",
        "_pre_attach_children('sub0B', ('sub0',))",
        "_pre_detach_children('sub0B', ())",
        "_post_detach_children('sub0B', ())",
        "_pre_attach_children('sub0B', ())",
        "_post_attach_children('sub0B', ())",
    ]
    TNode.TRACKING.clear()

    root.children = [s0, s1]

    assert TNode.TRACKING == [
        "_pre_detach_children('root', ('sub0', 'sub0A'))",
        "_pre_detach('sub0', 'root')",
        "_post_detach('sub0', 'root')",
        "_pre_detach('sub0A', 'root')",
        "_post_detach('sub0A', 'root')",
        "_post_detach_children('root', ('sub0', 'sub0A'))",
        "_pre_attach_children('root', ('sub0', 'sub0A'))",
        "_pre_attach('sub0', 'root')",
        "_post_attach('sub0', 'root')",
        "_pre_attach('sub0A', 'root')",
        "_post_attach('sub0A', 'root')",
        "_post_attach_children('root', ('sub0', 'sub0A'))",
    ]
    TNode.TRACKING.clear()

    s0.children = [s0a]

    assert TNode.TRACKING == [
        "_pre_detach_children('sub0', ('sub0B',))",
        "_pre_detach('sub0B', 'sub0')",
        "_post_detach('sub0B', 'sub0')",
        "_post_detach_children('sub0', ('sub0B',))",
        "_pre_attach_children('sub0', ('sub0B',))",
        "_pre_attach('sub0B', 'sub0')",
        "_post_attach('sub0B', 'sub0')",
        "_post_attach_children('sub0', ('sub0B',))",
    ]
    TNode.TRACKING.clear()

    s0a.children = [s1]

    assert TNode.TRACKING == [
        "_pre_detach_children('sub0B', ())",
        "_post_detach_children('sub0B', ())",
        "_pre_attach_children('sub0B', ('sub0A',))",
        "_pre_detach('sub0A', 'root')",
        "_post_detach('sub0A', 'root')",
        "_pre_attach('sub0A', 'sub0B')",
        "_post_attach('sub0A', 'sub0B')",
        "_post_attach_children('sub0B', ('sub0A',))",
    ]
    TNode.TRACKING.clear()

    root.children = [s0, s1]

    assert TNode.TRACKING == [
        "_pre_detach_children('root', ('sub0',))",
        "_pre_detach('sub0', 'root')",
        "_post_detach('sub0', 'root')",
        "_post_detach_children('root', ('sub0',))",
        "_pre_attach_children('root', ('sub0', 'sub0A'))",
        "_pre_attach('sub0', 'root')",
        "_post_attach('sub0', 'root')",
        "_pre_detach('sub0A', 'sub0B')",
        "_post_detach('sub0A', 'sub0B')",
        "_pre_attach('sub0A', 'root')",
        "_post_attach('sub0A', 'root')",
        "_post_attach_children('root', ('sub0', 'sub0A'))",
    ]
    TNode.TRACKING.clear()
