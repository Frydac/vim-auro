from enum import Enum

Bt = Enum('BasenameTypeEnum', 'source test')

basename_types = {
        Bt.source: ['.rb'],
        Bt.test: ['_tests.rb']
        }

Dt = Enum('DirTypeEnum', 'source test')

dir_types = {
        Dt.source: '{base_dir}/ruby/{namespace}',
        Dt.test: '{base_dir}/test/ruby/{namespace}'
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

infos = {}
infos['ruby'] = [None, related_source_info, related_test_info]



