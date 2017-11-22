from copy import deepcopy
from nose.tools import eq_

from anytree.exporter import DictExporter
from anytree.importer import DictImporter



def test_dict_importer():
    """Dict Importer."""
    importer = DictImporter()
    exporter = DictExporter()
    refdata = {
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
    data = deepcopy(refdata)
    root = importer.import_(data)
    eq_(data, refdata)
    eq_(exporter.export(root), data)

