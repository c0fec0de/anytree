# -*- coding: utf-8 -*-


from __future__ import print_function

import re

from .config import ASSERTIONS

_MAXCACHE = 20


class Resolver:
    """
    Resolve :any:`NodeMixin` paths using attribute `pathattr`.

    Keyword Args:
        name (str): Name of the node attribute to be used for resolving
        ignorecase (bool): Enable case insensisitve handling.
    """

    _match_cache = {}

    def __init__(self, pathattr="name", ignorecase=False):
        super(Resolver, self).__init__()
        self.pathattr = pathattr
        self.ignorecase = ignorecase

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

        Going above the root node raises a :any:`RootResolverError`:

        >>> r.get(top, "..")
        Traceback (most recent call last):
            ...
        anytree.resolver.RootResolverError: Cannot go above root node Node('/top')

        .. note:: Please not that :any:`get()` returned `None` in exactly that case above,
                  which was a bug until version 1.8.1.

        Case insensitive matching:

        >>> r.get(top, '/TOP')
        Traceback (most recent call last):
            ...
        anytree.resolver.ResolverError: unknown root node '/TOP'. root is '/top'.

        >>> r = Resolver('name', ignorecase=True)
        >>> r.get(top, '/TOp')
        Node('/top')
        """
        node, parts = self.__start(node, path, self.__cmp)
        for part in parts:
            if part == "..":
                parent = node.parent
                if parent is None:
                    raise RootResolverError(node)
                node = parent
            elif part in ("", "."):
                pass
            else:
                node = self.__get(node, part)
        return node

    def __get(self, node, name):
        namestr = str(name)
        for child in node.children:
            if self.__cmp(_getattr(child, self.pathattr), namestr):
                return child
        raise ChildResolverError(node, name, self.pathattr)

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

        Going above the root node raises a :any:`RootResolverError`:

        >>> r.glob(top, "..")
        Traceback (most recent call last):
            ...
        anytree.resolver.RootResolverError: Cannot go above root node Node('/top')
        """
        node, parts = self.__start(node, path, self.__match)
        return self.__glob(node, parts)

    def __start(self, node, path, cmp_):
        sep = node.separator
        parts = path.split(sep)
        # resolve root
        if path.startswith(sep):
            node = node.root
            rootpart = _getattr(node, self.pathattr)
            parts.pop(0)
            if not parts[0]:
                msg = "root node missing. root is '%s%s'."
                raise ResolverError(node, "", msg % (sep, str(rootpart)))
            if not cmp_(rootpart, parts[0]):
                msg = "unknown root node '%s%s'. root is '%s%s'."
                raise ResolverError(node, "", msg % (sep, parts[0], sep, str(rootpart)))
            parts.pop(0)
        return node, parts

    def __glob(self, node, parts):
        if ASSERTIONS:  # pragma: no branch
            assert node is not None
        nodes = []
        if parts:
            name = parts[0]
            remainder = parts[1:]
            # handle relative
            if name == "..":
                parent = node.parent
                if parent is None:
                    raise RootResolverError(node)
                nodes += self.__glob(parent, remainder)
            elif name in ("", "."):
                nodes += self.__glob(node, remainder)
            else:
                matches = self.__find(node, name, remainder)
                if not matches and not Resolver.is_wildcard(name):
                    raise ChildResolverError(node, name, self.pathattr)
                nodes += matches
        else:
            nodes = [node]
        return nodes

    def __find(self, node, pat, remainder):
        matches = []
        for child in node.children:
            name = _getattr(child, self.pathattr)
            try:
                if self.__match(name, pat):
                    if remainder:
                        matches += self.__glob(child, remainder)
                    else:
                        matches.append(child)
            except ResolverError as exc:
                if not Resolver.is_wildcard(pat):
                    raise exc
        return matches

    @staticmethod
    def is_wildcard(path):
        """Return `True` is a wildcard."""
        return "?" in path or "*" in path

    def __match(self, name, pat):
        k = (pat, self.ignorecase)
        try:
            re_pat = Resolver._match_cache[k]
        except KeyError:
            res = Resolver.__translate(pat)
            if len(Resolver._match_cache) >= _MAXCACHE:
                Resolver._match_cache.clear()
            flags = 0
            if self.ignorecase:
                flags |= re.IGNORECASE
            Resolver._match_cache[k] = re_pat = re.compile(res, flags=flags)
        return re_pat.match(name) is not None

    def __cmp(self, name, pat):
        if self.ignorecase:
            return name.upper() == pat.upper()
        return name == pat

    @staticmethod
    def __translate(pat):
        re_pat = ""
        for char in pat:
            if char == "*":
                re_pat += ".*"
            elif char == "?":
                re_pat += "."
            else:
                re_pat += re.escape(char)
        return r"(?ms)" + re_pat + r"\Z"


class ResolverError(RuntimeError):
    def __init__(self, node, child, msg):
        """Resolve Error at `node` handling `child`."""
        super(ResolverError, self).__init__(msg)
        self.node = node
        self.child = child


class RootResolverError(ResolverError):
    def __init__(self, root):
        """Root Resolve Error, cannot go above root node."""
        msg = "Cannot go above root node %r" % (root,)
        super(RootResolverError, self).__init__(root, None, msg)


class ChildResolverError(ResolverError):
    def __init__(self, node, child, pathattr):
        """Child Resolve Error at `node` handling `child`."""
        names = [repr(_getattr(c, pathattr)) for c in node.children]
        msg = "%r has no child %s. Children are: %s." % (node, child, ", ".join(names))
        super(ChildResolverError, self).__init__(node, child, msg)


def _getattr(node, name):
    return str(getattr(node, name, None))
