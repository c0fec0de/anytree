import json

from .dictexporter import DictExporter


class JsonExporter(object):

    def __init__(self, dictexporter=None, **kwargs):
        """
        Tree to JSON exporter.

        The tree is converted to a dictionary via `dictexporter` and exported to JSON.

        Keyword Arguments:
            dictexporter: Dictionary Exporter used (see :any:`DictExporter`).
            kwargs: All other arguments are passed to
                    :any:`json.dump`/:any:`json.dumps`.
                    See documentation for reference.

        >>> from anytree import AnyNode
        >>> from anytree.exporter import JsonExporter
        >>> root = AnyNode(a="root")
        >>> s0 = AnyNode(a="sub0", parent=root)
        >>> s0a = AnyNode(a="sub0A", b="foo", parent=s0)
        >>> s0b = AnyNode(a="sub0B", parent=s0)
        >>> s1 = AnyNode(a="sub1", parent=root)

        >>> exporter = JsonExporter(indent=2, sort_keys=True)
        >>> print(exporter.export(root))
        {
          "a": "root",
          "children": [
            {
              "a": "sub0",
              "children": [
                {
                  "a": "sub0A",
                  "b": "foo"
                },
                {
                  "a": "sub0B"
                }
              ]
            },
            {
              "a": "sub1"
            }
          ]
        }
        """
        self.dictexporter = dictexporter
        self.kwargs = kwargs

    def export(self, node):
        """Return JSON for tree starting at `node`."""
        dictexporter = self.dictexporter or DictExporter()
        data = dictexporter.export(node)
        return json.dumps(data, **self.kwargs)

    def write(self, node, filehandle):
        """Write JSON to `filehandle` starting at `node`."""
        dictexporter = self.dictexporter or DictExporter()
        data = dictexporter.export(node)
        return json.dump(data, filehandle, **self.kwargs)
