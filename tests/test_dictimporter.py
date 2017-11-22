from copy import deepcopy
from nose.tools import eq_

from anytree.exporter import DictExporter
from anytree.importer import DictImporter



def test_dict_importer():
    """Dict Importer."""
    importer = DictImporter()
    exporter = DictExporter()
    ref = {
        'id': 'root', 'children': [
            {'id': 'sub0', 'children': [
                {'id': 'sub0B'},
                {'id': 'sub0A'}
            ]},
            {'id': 'sub1', 'children': [
                {'id': 'sub1A'},
                {'id': 'sub1B'},
                {'id': 'sub1C', 'children': [
                    {'id': 'sub1Ca'}
                ]}
            ]}
        ]}
    data = deepcopy(ref)
    root = importer.import_(data)
    eq_(data, ref)
    eq_(exporter.export(root), data)

