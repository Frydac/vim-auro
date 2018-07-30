from pathlib import Path
from pprint import pprint
from auro.path import AuroPath, Ft
from typing import List
from enum import Enum

Bt = Enum('BasenameTypeEnum', 'hpp cpp c h test')

basename_types = {
        Bt.hpp:  ['.hpp', '.hxx'], # cpp headers
        Bt.cpp:  ['.cpp'],         # cpp source
        Bt.h:    ['.h'],           # c headers
        Bt.c:    ['.c', '.cc'],    # c source
        Bt.test: ['_tests.cpp']    # c and cpp test
        }

Dt = Enum('DirtypeEnum', 'public protected private test_public test_protected test_private')

dir_types = {
        Dt.public:         '{base_dir}/public/{namespace}',
        Dt.protected:      '{base_dir}/protected/{namespace}',
        Dt.private:        '{base_dir}/private/{namespace}',
        Dt.test_public:    '{base_dir}/test/private/{namespace}',
        Dt.test_protected: '{base_dir}/test/protected/{namespace}',
        Dt.test_private:   '{base_dir}/test/private/{namespace}'
        }

related_header_info = {
        'bt': [{'from': [Bt.cpp, Bt.test], 'to': [Bt.hpp]},
               {'from': [Bt.c, Bt.test],   'to': [Bt.h]}],

        'dt': [{'from': [Dt.public, Dt.test_public],       'to': [Dt.public]},
               {'from': [Dt.protected, Dt.test_protected], 'to': [Dt.protected, Dt.public]},
               {'from': [Dt.private],                      'to': [Dt.private, Dt.public]},
               {'from': [Dt.test_private],                 'to': [Dt.private, Dt.protected, Dt.public]}],
        'basename_types': basename_types,
        'dir_types': dir_types
        }

related_source_info = {
        'bt':[{'from': [Bt.h, Bt.test, Bt.hpp], 'to': [Bt.cpp]},
              {'from': [Bt.h, Bt.test],         'to': [Bt.c]}],
        'dt':[{'from': [Dt.public, Dt.test_public], 'to': [Dt.public, Dt.protected, Dt.private]},
              {'from': [Dt.protected],              'to': [Dt.protected]},
              {'from': [Dt.private],                'to': [Dt.private]},
              {'from': [Dt.test_private],           'to': [Dt.private, Dt.protected, Dt.public]},
              {'from': [Dt.test_protected],         'to': [Dt.protected, Dt.public]}],
        'basename_types': basename_types,
        'dir_types': dir_types
        }

related_test_info = {
        'bt':[{'from': [Bt.h, Bt.hpp, Bt.c, Bt.cpp], 'to': [Bt.test]} ],
        'dt':[{'from': [Dt.public],    'to': [Dt.test_public, Dt.private]},
              {'from': [Dt.protected], 'to': [Dt.test_protected]},
              {'from': [Dt.private],   'to': [Dt.test_private]}],
        'basename_types': basename_types,
        'dir_types': dir_types
        }

infos = [related_header_info, related_source_info, related_test_info]

