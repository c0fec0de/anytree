"""Access the owning node's child storage without changing its layout."""

_NODE_TYPES = None


def _get_children(node):
    global _NODE_TYPES  # noqa: PLW0603
    if _NODE_TYPES is None:
        # Imported once on use to avoid a cycle while the two mixins are defined.
        from .lightnodemixin import LightNodeMixin  # pylint: disable=import-outside-toplevel
        from .nodemixin import NodeMixin  # pylint: disable=import-outside-toplevel

        _NODE_TYPES = (NodeMixin, LightNodeMixin)
    normal_type, light_type = _NODE_TYPES
    if isinstance(node, normal_type) and (
        not isinstance(node, light_type) or type(node).__mro__.index(normal_type) < type(node).__mro__.index(light_type)
    ):
        return node._NodeMixin__children_or_empty  # pylint: disable=protected-access
    return node._LightNodeMixin__children_or_empty  # pylint: disable=protected-access
