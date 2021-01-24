# -*- coding: utf-8 -*-
from anytree import Node


class IndentedTextImporter(object):

    def __init__(self, rootname="root"):
        u"""
        Import Tree from indented text.

        Every line of text is converted to an instance of Node.
        The text of the lines establish the names of the nodes.
        Indentation establishes the hierarchy between the nodes.

        White space must be all spaces, and what constitutes
        indentation must be consistent -- That is, if you use x2
        spaces to establish 1 level of indentation, then all
        indentations much be x2 spaces.  The first found indentation
        sets the model for all further indentation.

        (If you wish to use this with tabs, simply replace the input
         text string's leading tabs with spaces, before use.
         This may be as simple as s.replace("\t", "  "), if the only
         tabs used are used for indentation.)

        The name for a root node must be supplied;
        Every line starting at column 0 is a child of this root node.

        Keyword Args:
            rootname: name for the root node (invisible)

        >>> from anytree.importer import IndentedTextImporter
        >>> from anytree import RenderTree
        >>> importer = IndentedTextImporter("root")
        >>> data = '''
        ... sub0
        ...   sub0A
        ...   sub0B
        ... sub1
        ... '''
        >>> root = importer.import_(data)
        >>> print(RenderTree(root))
        Node('/root')
        ├── Node('/root/sub0')
        │   ├── Node('/root/sub0/sub0A')
        │   └── Node('/root/sub0/sub0B')
        └── Node('/root/sub1')
        """
        self.rootname = rootname

    def import_(self, text):
        """Import tree from `text`."""
        expected_indentation = None
        root = Node(self.rootname)  # node implied at "column -(INDENTx1)"
        n = None  # last node's indentation level
        parents_at_levels = [root]  # parents at indentation levels
        for i, line in enumerate(text.splitlines()):
            sp = len(line) - len(line.lstrip(" "))
            name = line[sp:]
            if not name:  # blank line
                continue
            if sp > 0 and expected_indentation is None:  # FIRST indent
                expected_indentation = sp  # imprint from first indent
                n = 0  # last indentation was 0
            if expected_indentation is None and sp == 0:
                node = Node(name, parent=root)
                if len(parents_at_levels) == 1:
                    parents_at_levels.append(node)  # first time
                elif len(parents_at_levels) == 2:
                    parents_at_levels[-1] = node  # still no expectation
            elif expected_indentation is None:
                raise IndentedTextImporterError("bad indent at line", i)
            elif sp == n+expected_indentation:
                node = Node(name, parent=parents_at_levels[-1])
                parents_at_levels.append(node)
            elif sp == n:
                node = Node(name, parent=parents_at_levels[-2])
                parents_at_levels[-1] = node  # replace prior end
            elif (sp < n) and (sp % expected_indentation == 0):
                prior_levels = n // expected_indentation
                levels = sp // expected_indentation
                node = Node(name, parent=parents_at_levels[levels])
                parents_at_levels[levels+1:] = [node]  # replace dismissed
            else:
                raise IndentedTextImporterError("bad indent at line", i)
            n = sp
        return root


class IndentedTextImporterError(RuntimeError):
    """IndentedTextImporter Error."""
