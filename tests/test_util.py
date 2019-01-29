# -*- coding: utf-8 -*-
from nose.tools import eq_

from anytree.util import commonancestors
from anytree import Node


def test_commonancestors():
    """commonancestors."""
    udo = Node("Udo")
    marc = Node("Marc", parent=udo)
    dan = Node("Dan", parent=udo)
    jet = Node("Jet", parent=dan)
    joe = Node("Joe", parent=dan)

    eq_(commonancestors(jet, joe), (udo, dan))
    eq_(commonancestors(jet, marc), (udo,))
    eq_(commonancestors(jet), (udo, dan))
    eq_(commonancestors(), ())
