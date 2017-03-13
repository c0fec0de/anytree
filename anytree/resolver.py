# -*- coding: utf-8 -*-


from __future__ import print_function
try:  # pragma: no cover
    from collections import OrderedDict
except ImportError:  # pragma: no cover
    from ordereddict import OrderedDict

import re

_MAXCACHE = 20


class Resolver(object):

    _match_cache = {}

    def __init__(self, pathattr='name'):
        """Resolve :any:`NodeMixin` paths using attribute `pathattr`."""
        super(Resolver, self).__init__()
        self.pathattr = pathattr

    def get(self, node, path):
        """
        Return instance at `path`.

        An example module tree:

        >>> from anytree import Node
        >>> top = Node("top", parent=None)
        >>> sub0 = Node("sub0", parent=top)
        >>> sub0sub0 = Node("sub0sub0", parent=sub0)
        >>> sub0sub1 = Node("sub0sub1", parent=sub0)
        >>> sub1 = Node("sub1", parent=top)

        A resolver using the `name` attribute:

        >>> r = Resolver('name')

        Relative paths:

        >>> r.get(top, "sub0/sub0sub0")
        Node('/top/sub0/sub0sub0')
        >>> r.get(sub1, "..")
        Node('/top')
        >>> r.get(sub1, "../sub0/sub0sub1")
        Node('/top/sub0/sub0sub1')
        >>> r.get(sub1, ".")
        Node('/top/sub1')
        >>> r.get(sub1, "")
        Node('/top/sub1')
        >>> r.get(top, "sub2")
        Traceback (most recent call last):
          ...
        anytree.resolver.ChildResolverError: Node('/top') has no child sub2. Children are: 'sub0', 'sub1'.

        Absolute paths:

        >>> r.get(sub0sub0, "/top")
        Node('/top')
        >>> r.get(sub0sub0, "/top/sub0")
        Node('/top/sub0')
        >>> r.get(sub0sub0, "/")
        Traceback (most recent call last):
          ...
        anytree.resolver.ResolverError: root node missing. root is '/top'.
        >>> r.get(sub0sub0, "/bar")
        Traceback (most recent call last):
          ...
        anytree.resolver.ResolverError: unknown root node '/bar'. root is '/top'.
        """
        node, parts = self.__start(node, path)
        for part in parts:
            if part == "..":
                node = node.parent
            elif part in ("", "."):
                pass
            else:
                nodemap = self.__get_nodemap(node)
                try:
                    node = nodemap[part]
                except KeyError:
                    raise ChildResolverError(node, part, nodemap.keys())
        return node

    def glob(self, node, path):
        """
        Return instances at `path` supporting wildcards.

        Behaves identical to :any:`get`, but accepts wildcards and returns
        a list of found nodes.

        * `*` matches any characters, except '/'.
        * `?` matches a single character, except '/'.

        An example module tree:

        >>> from anytree import Node
        >>> top = Node("top", parent=None)
        >>> sub0 = Node("sub0", parent=top)
        >>> sub0sub0 = Node("sub0", parent=sub0)
        >>> sub0sub1 = Node("sub1", parent=sub0)
        >>> sub1 = Node("sub1", parent=top)
        >>> sub1sub0 = Node("sub0", parent=sub1)

        A resolver using the `name` attribute:

        >>> r = Resolver('name')

        Relative paths:

        >>> r.glob(top, "sub0/sub?")
        [Node('/top/sub0/sub0'), Node('/top/sub0/sub1')]
        >>> r.glob(sub1, ".././*")
        [Node('/top/sub0'), Node('/top/sub1')]
        >>> r.glob(top, "*/*")
        [Node('/top/sub0/sub0'), Node('/top/sub0/sub1'), Node('/top/sub1/sub0')]
        >>> r.glob(top, "*/sub0")
        [Node('/top/sub0/sub0'), Node('/top/sub1/sub0')]
        >>> r.glob(top, "sub1/sub1")
        Traceback (most recent call last):
            ...
        anytree.resolver.ChildResolverError: Node('/top/sub1') has no child sub1. Children are: 'sub0'.

        Non-matching wildcards are no error:

        >>> r.glob(top, "bar*")
        []
        >>> r.glob(top, "sub2")
        Traceback (most recent call last):
          ...
        anytree.resolver.ChildResolverError: Node('/top') has no child sub2. Children are: 'sub0', 'sub1'.

        Absolute paths:

        >>> r.glob(sub0sub0, "/top/*")
        [Node('/top/sub0'), Node('/top/sub1')]
        >>> r.glob(sub0sub0, "/")
        Traceback (most recent call last):
          ...
        anytree.resolver.ResolverError: root node missing. root is '/top'.
        >>> r.glob(sub0sub0, "/bar")
        Traceback (most recent call last):
          ...
        anytree.resolver.ResolverError: unknown root node '/bar'. root is '/top'.
        """
        node, parts = self.__start(node, path)
        return self.__glob(node, parts)

    def __start(self, node, path):
        parts = path.split("/")
        if path.startswith("/"):
            node = node.root
            rootpart = self.__get_part(node)
            parts.pop(0)
            if not parts[0]:
                msg = "root node missing. root is '/%s'."
                raise ResolverError(node, "", msg % str(rootpart))
            elif parts[0] != rootpart:
                msg = "unknown root node '/%s'. root is '/%s'."
                raise ResolverError(node, "", msg % (parts[0], str(rootpart)))
            parts.pop(0)
        return node, parts

    def __get_nodemap(self, node):
        subnodes = [(self.__get_part(child), child)
                    for child in node.children]
        return OrderedDict(subnodes)

    def __glob(self, node, parts):
        nodes = []
        part = parts[0]
        remainparts = parts[1:]
        # handle relative
        if part == "..":
            nodes += self.__glob(node.parent, remainparts)
        elif part in ("", "."):
            nodes += self.__glob(node, remainparts)
        else:
            matches = []
            nodemap = self.__get_nodemap(node)
            for name, child in nodemap.items():
                try:
                    if Resolver.__match(name, part):
                        if remainparts:
                            matches += self.__glob(child, remainparts)
                        else:
                            matches.append(child)
                except ResolverError as exc:
                    if not Resolver.__is_wildcard(part):
                        raise exc
            if not matches and not Resolver.__is_wildcard(part):
                raise ChildResolverError(node, part, nodemap.keys())
            nodes += matches
        return nodes

    def __get_part(self, node):
        return getattr(node, self.pathattr)

    @staticmethod
    def __is_wildcard(pat):
        return "?" in pat or "*" in pat

    @staticmethod
    def __match(name, pat):
        try:
            re_pat = Resolver._match_cache[pat]
        except KeyError:
            res = Resolver.__translate(pat)
            if len(Resolver._match_cache) >= _MAXCACHE:
                Resolver._match_cache.clear()
            Resolver._match_cache[pat] = re_pat = re.compile(res)
        return re_pat.match(name) is not None

    @staticmethod
    def __translate(pat):
        re_pat = ''
        for char in pat:
            if char == "*":
                re_pat += ".*"
            elif char == "?":
                re_pat += "."
            else:
                re_pat += re.escape(char)
        return re_pat + '\Z(?ms)'


class ResolverError(RuntimeError):

    def __init__(self, node, child, msg):
        """Resolve Error at `node` handling `child`."""
        super(ResolverError, self).__init__(msg)
        self.node = node
        self.child = child


class ChildResolverError(ResolverError):

    def __init__(self, node, child, children):
        """Child Resolve Error at `node` handling `child` with known `children`."""
        names = ", ".join([repr(c) for c in children])
        msg = "%r has no child %s. Children are: %s."
        msg = msg % (node, child, names)
        super(ChildResolverError, self).__init__(node, child, msg)
