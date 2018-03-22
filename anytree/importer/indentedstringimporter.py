# -*- coding: utf-8 -*-
from anytree import AnyNode


def _get_indentation(line):
    content = line.lstrip(' ')
    # Split string using version without indentation; First item of result is the indentation itself.
    indentation_length = len(line.split(content)[0])
    return indentation_length, content


class IndentedStringImporter(object):

    def __init__(self, nodecls=AnyNode):
        u"""
        Import Tree from a single string (with all the lines) or list of strings (lines) with indentation.

        Every indented line is converted to an instance of `nodecls`. The string (without indentation) found on the lines are set as the respective node name.

        This importer do not constrain indented data to have a definite number of whitespaces (multiple of any number). Nodes are considered child of a parent simply if its indentation is bigger than its parent.

        This means that the tree can have siblings with different indentations, as long as the siblings indentations are bigger than the respective parent (but not necessarily the same considering each other).

        Keyword Args:
            nodecls: class used for nodes.

        Example using a string list:

        >>> from anytree.importer import IndentedStringImporter
        >>> from anytree import RenderTree
        >>> importer = IndentedStringImporter()
        >>> lines = [
        ...    'Node1',
        ...    'Node2',
        ...    '    Node3',
        ...    'Node5',
        ...    '    Node6',
        ...    '        Node7',
        ...    '    Node8',
        ...    '        Node9',
        ...    '      Node10',
        ...    '    Node11',
        ...    '  Node12',
        ...    'Node13',
        ...]
        >>> root = importer.import_(lines)
        >>> print(RenderTree(root))
       AnyNode(name='root')
        ├── AnyNode(name='Node1')
        ├── AnyNode(name='Node2')
        │   └── AnyNode(name='Node3')
        ├── AnyNode(name='Node5')
        │   ├── AnyNode(name='Node6')
        │   │   └── AnyNode(name='Node7')
        │   ├── AnyNode(name='Node8')
        │   │   ├── AnyNode(name='Node9')
        │   │   └── AnyNode(name='Node10')
        │   ├── AnyNode(name='Node11')
        │   └── AnyNode(name='Node12')
        └── AnyNode(name='Node13')

        Example using a string:

        >>> string = "Node1\n  Node2\n  Node3\n    Node4"
        >>> root = importer.import_(string)
        >>> print(RenderTree(root))
         AnyNode(name='root')
        └── AnyNode(name='Node1')
            ├── AnyNode(name='Node2')
            └── AnyNode(name='Node3')
                └── AnyNode(name='Node4')
        """
        self.nodecls = nodecls

    def _tree_from_indented_str(self, data):
        if isinstance(data, str):
            lines = data.splitlines()
        else:
            lines = data
        root = self.nodecls(name="root")
        indentations = {}
        for line in lines:
            current_indentation, name = _get_indentation(line)

            if len(indentations) == 0:
                parent = root
            elif current_indentation not in indentations:
                # parent is the next lower indentation
                keys = [key for key in indentations.keys() if key < current_indentation]
                parent = indentations[max(keys)]
            else:
                # current line uses the parent of the last line with same indentation and replaces
                # it as the last line with this given indentation
                parent = indentations[current_indentation].parent

            indentations[current_indentation] = self.nodecls(name=name, parent=parent)

            # delete all higher indentations
            keys = [key for key in indentations.keys() if key > current_indentation]
            for key in keys:
                indentations.pop(key)
        return root

    def import_(self, data):
        """Import tree from `data`, which can be a single string or a list of lines."""
        return self._tree_from_indented_str(data)
