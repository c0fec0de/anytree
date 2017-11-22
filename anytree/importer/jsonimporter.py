import json

from .dictimporter import DictImporter


class JsonImporter(object):

    def __init__(self, dictimporter=None, **kwargs):
        u"""
        Import Tree from JSON.

        The JSON is read and converted to a dictionary via `dictimporter`.

        Keyword Arguments:
            dictimporter: Dictionary Importer used (see :any:`DictImporter`).
            kwargs: All other arguments are passed to
                    :any:`json.load`/:any:`json.loads`.
                    See documentation for reference.

        >>> from anytree.importer import JsonImporter
        >>> from anytree import RenderTree
        >>> importer = JsonImporter()
        >>> data = '''
        ... {
        ...   "a": "root",
        ...   "children": [
        ...     {
        ...       "a": "sub0",
        ...       "children": [
        ...         {
        ...           "a": "sub0A",
        ...           "b": "foo"
        ...         },
        ...         {
        ...           "a": "sub0B"
        ...         }
        ...       ]
        ...     },
        ...     {
        ...       "a": "sub1"
        ...     }
        ...   ]
        ... }'''
        >>> root = importer.import_(data)
        >>> print(RenderTree(root))
        AnyNode(a='root')
        ├── AnyNode(a='sub0')
        │   ├── AnyNode(a='sub0A', b='foo')
        │   └── AnyNode(a='sub0B')
        └── AnyNode(a='sub1')
        """
        self.dictimporter = dictimporter
        self.kwargs = kwargs

    def import_(self, data):
        """Read JSON from `data`."""
        dictimporter = self.dictimporter or DictImporter()
        data = json.loads(data, **self.kwargs)
        return dictimporter.import_(data)

    def read(self, filehandle):
        """Read JSON from `filehandle`."""
        dictimporter = self.dictimporter or DictImporter()
        data = json.load(filehandle, **self.kwargs)
        return dictimporter.import_(data)
