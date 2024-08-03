"""
Node Classes.

* :any:`AnyNode`: a generic tree node with any number of attributes.
* :any:`Node`: a simple tree node with at least a name attribute and any number of additional attributes.
* :any:`NodeMixin`: extends any python class to a tree node.
* :any:`SymlinkNode`: Tree node which references to another tree node.
* :any:`SymlinkNodeMixin`: extends any Python class to a symbolic link to a tree node.
* :any:`LightNodeMixin`: A :any:`NodeMixin` using slots.
"""

# pylint: disable=useless-import-alias
from .anynode import AnyNode as AnyNode  # noqa
from .exceptions import LoopError as LoopError  # noqa
from .exceptions import TreeError as TreeError  # noqa
from .lightnodemixin import LightNodeMixin as LightNodeMixin  # noqa
from .node import Node as Node  # noqa
from .nodemixin import NodeMixin as NodeMixin  # noqa
from .symlinknode import SymlinkNode as SymlinkNode  # noqa
from .symlinknodemixin import SymlinkNodeMixin as SymlinkNodeMixin  # noqa
