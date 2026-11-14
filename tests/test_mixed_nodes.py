"""Keep normal and slotted nodes coherent in mixed trees."""

import copy
import pickle

import pytest

from anytree import AnyNode, LightNodeMixin, LoopError, Node, NodeMixin, PreOrderIter, SymlinkNode


class LightNode(LightNodeMixin):
    """A genuinely slotted node with no instance dictionary."""

    __slots__ = ("name",)

    def __init__(self, name, parent=None):
        """Store the name and optionally attach to a parent."""
        self.name = name
        self.parent = parent


def make_any(name, parent=None):
    """Create an AnyNode with the same constructor interface."""
    return AnyNode(name=name, parent=parent)


def make_link(name, parent=None):
    """Create a link whose own parent must not affect its target."""
    return SymlinkNode(Node(name), parent=parent)


FACTORIES = (Node, make_any, LightNode, make_link)


@pytest.mark.parametrize("parentcls", FACTORIES)
@pytest.mark.parametrize("childcls", FACTORIES)
def test_attach_and_detach(parentcls, childcls):
    """Every pairing keeps both sides of a relationship in sync."""
    parent = parentcls("root")
    child = childcls("child", parent=parent)
    assert parent.children == (child,)
    assert child.parent is parent
    assert child.path == (parent, child)
    assert list(PreOrderIter(parent)) == [parent, child]
    child.parent = None
    assert parent.children == ()
    assert child.parent is None
    if isinstance(child, LightNode):
        assert not hasattr(child, "__dict__")


@pytest.mark.parametrize("parentcls,othercls", [(Node, LightNode), (LightNode, Node)])
@pytest.mark.parametrize("childcls", FACTORIES)
def test_reparent_between_storage_types(parentcls, othercls, childcls):
    """Moving a node removes it from the old parent's real child container."""
    parent = parentcls("old")
    other = othercls("new")
    before = parentcls("before", parent=parent)
    child = childcls("child", parent=parent)
    after = parentcls("after", parent=parent)
    child.parent = other
    assert parent.children == (before, after)
    assert other.children == (child,)
    assert child.parent is other
    assert child.path == (other, child)
    del other.children
    assert other.children == ()
    assert child.parent is None


@pytest.mark.parametrize("parentcls", FACTORIES)
def test_mixed_children_assignment_and_order(parentcls):
    """Batch assignment can mix types and preserve explicit order."""
    parent = parentcls("root")
    children = tuple(cls(str(idx)) for idx, cls in enumerate(FACTORIES))
    parent.children = children
    assert parent.children == children
    assert all(child.parent is parent for child in children)
    parent.children = tuple(reversed(children))
    assert parent.children == tuple(reversed(children))
    del parent.children
    assert all(child.parent is None for child in children)


@pytest.mark.parametrize("rootcls,childcls", [(Node, LightNode), (LightNode, Node)])
def test_mixed_cycle_rejected_without_changing_tree(rootcls, childcls):
    """Cycle protection still checks identities across node implementations."""
    root = rootcls("root")
    child = childcls("child", parent=root)
    grandchild = rootcls("grandchild", parent=child)
    with pytest.raises(LoopError):
        root.parent = grandchild
    assert root.parent is None
    assert root.children == (child,)
    assert child.children == (grandchild,)


@pytest.mark.parametrize("rootcls,childcls", [(Node, LightNode), (LightNode, Node)])
@pytest.mark.parametrize("clone", [copy.deepcopy, lambda node: pickle.loads(pickle.dumps(node))])
def test_mixed_copy_and_pickle(rootcls, childcls, clone):
    """Existing slot and dictionary storage survives a mixed-tree round trip."""
    root = rootcls("root")
    child = childcls("child", parent=root)
    rootcls("grandchild", parent=child)
    result = clone(root)
    assert [node.name for node in PreOrderIter(result)] == ["root", "child", "grandchild"]
    resultchild = result.children[0]
    assert resultchild.parent is result
    resultchild.parent = None
    assert result.children == ()
    assert child.parent is root


class EqualLightNode(LightNode):
    """Distinct nodes may compare equal without sharing a position."""

    __slots__ = ()

    def __eq__(self, other):
        """Compare names, deliberately not identities."""
        return isinstance(other, EqualLightNode) and self.name == other.name

    __hash__ = None


@pytest.mark.parametrize("parentcls", [Node, LightNode])
def test_detach_uses_identity_not_equality(parentcls):
    """Removing one equal child must keep its distinct equal sibling."""
    parent = parentcls("root")
    first = EqualLightNode("same", parent=parent)
    second = EqualLightNode("same", parent=parent)
    first.parent = None
    assert len(parent.children) == 1
    assert parent.children[0] is second
    assert second.parent is parent


def test_symlink_parent_does_not_change_target_children():
    """Mixed child storage belongs to the link, never to its target."""
    target = Node("target")
    targetchild = Node("targetchild", parent=target)
    link = SymlinkNode(target)
    child = LightNode("child", parent=link)
    assert link.children == (child,)
    assert target.children == (targetchild,)
    child.parent = None
    assert link.children == ()
    assert target.children == (targetchild,)


class NormalFirstNode(NodeMixin, LightNodeMixin):
    """A dual-mixin node whose normal properties win in its MRO."""

    def __init__(self, name, parent=None):
        """Initialize through the selected parent property."""
        self.name = name
        self.parent = parent


class LightFirstNode(LightNodeMixin, NodeMixin):
    """A dual-mixin node whose slotted properties win in its MRO."""

    def __init__(self, name, parent=None):
        """Initialize through the selected parent property."""
        self.name = name
        self.parent = parent


@pytest.mark.parametrize("parentcls", [NormalFirstNode, LightFirstNode])
@pytest.mark.parametrize("childcls", [Node, LightNode, NormalFirstNode, LightFirstNode])
def test_dual_mixin_parents_use_mro_storage(parentcls, childcls):
    """Storage selection follows whichever children property the MRO selects."""
    parent = parentcls("root")
    child = childcls("child", parent=parent)
    assert parent.children == (child,)
    assert child.parent is parent
    child.parent = None
    assert parent.children == ()
