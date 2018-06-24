
def commonancestors(*nodes):
    """
    Determine common ancestors of `nodes`.

    >>> from anytree import Node
    >>> udo = Node("Udo")
    >>> marc = Node("Marc", parent=udo)
    >>> lian = Node("Lian", parent=marc)
    >>> dan = Node("Dan", parent=udo)
    >>> jet = Node("Jet", parent=dan)
    >>> jan = Node("Jan", parent=dan)
    >>> joe = Node("Joe", parent=dan)

    >>> commonancestors(jet, joe)
    (Node('/Udo'), Node('/Udo/Dan'))
    >>> commonancestors(jet, marc)
    (Node('/Udo'),)
    >>> commonancestors(jet)
    (Node('/Udo'), Node('/Udo/Dan'))
    >>> commonancestors()
    ()
    """
    ancestors = [node.ancestors for node in nodes]
    common = []
    for parentnodes in zip(*ancestors):
        parentnode = parentnodes[0]
        if all([parentnode is p for p in parentnodes[1:]]):
            common.append(parentnode)
        else:
            break
    return tuple(common)
