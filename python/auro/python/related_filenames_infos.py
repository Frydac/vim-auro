from enum import Enum

Bt = Enum('BasenameTypeEnum', 'source test')

basename_matchers = {
        Bt.source: ['.py'],
        Bt.test: ['test_{name}.py', '_test.py']
        }

Dt = Enum('DirnameTypeEnum', 'source test')

dirname_matchers = {
        Dt.source: '{base_dir}/python/{namespace}',
        Dt.test: '{base_dir}/test/python/{namespace}'
        }

related_source_info = {
        'basename_mapping':  [{'from': [Bt.test], 'to': [Bt.source]}],
        'dirname_mapping':   [{'from': [Dt.test], 'to': [Dt.source]}],
        'basename_matchers': basename_matchers,
        'dirname_matchers':  dirname_matchers
        }

related_test_info = {
        'basename_mapping':  [{'from': [Bt.source], 'to': [Bt.test]}],
        'dirname_mapping':   [{'from': [Dt.source], 'to': [Dt.test]}],
        'basename_matchers': basename_matchers,
        'dirname_matchers':  dirname_matchers
        }

infos = {}
infos['python'] = [None, related_source_info, related_test_info]



