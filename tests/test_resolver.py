# -*- coding: utf-8 -*-
from nose.tools import eq_

import anytree as at


def test_wildcard_cache():
    """Wildcard Cache."""
    root = at.Node("root")
    sub0 = at.Node("sub0", parent=root)
    sub1 = at.Node("sub1", parent=root)
    r = at.Resolver()
    # strip down cache size
    at._MAXCACHE = 2
    at.Resolver._match_cache.clear()
    eq_(len(at.Resolver._match_cache), 0)
    eq_(r.glob(root, "sub0"), [sub0])
    eq_(len(at.Resolver._match_cache), 1)
    eq_(r.glob(root, "sub1"), [sub1])
    eq_(len(at.Resolver._match_cache), 2)
    eq_(r.glob(root, "sub*"), [sub0, sub1])
    eq_(len(at.Resolver._match_cache), 1)
