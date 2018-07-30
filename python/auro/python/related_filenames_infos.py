from enum import Enum

Bt = Enum('BasenameTypeEnum', 'source test')

basename_types = {
        Bt.source: ['.py'],
        Bt.test: ['test_{name}.py']
        }

Dt = Enum('DirTypeEnum', 'source test')

dir_types = {
        Dt.source: '{base_dir}/python/{namespace}',
        Dt.test: '{base_dir}/python/test/{namespace}'
        }

related_source_info = {
        'bt':             [{'from': [Bt.test], 'to': [Bt.source]}],
        'dt':             [{'from': [Dt.test], 'to': [Dt.source]}],
        'basename_types': basename_types,
        'dir_types':      dir_types
        }

related_test_info = {
        'bt':             [{'from': [Bt.source], 'to': [Bt.test]}],
        'dt':             [{'from': [Dt.source], 'to': [Dt.test]}],
        'basename_types': basename_types,
        'dir_types':      dir_types
        }

infos = [None, related_source_info, related_test_info]



