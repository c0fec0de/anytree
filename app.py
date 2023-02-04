from anytree import Node
from anytree.exporter import MermaidExporter
import pathlib

pwd = pathlib.Path(__file__).parent.resolve()

root = Node("root")
s0 = Node("sub0", parent=root)
Node("sub0B", parent=s0)
Node("sub0A", parent=s0)
s1 = Node("sub1", parent=root)
Node("sub1A", parent=s1)
Node("sub1B", parent=s1)
s1c = Node("sub1C", parent=s1)
Node(99, parent=s1c)

MermaidExporter(root).to_markdown_file((pwd / "mermaid_tree1.md"))