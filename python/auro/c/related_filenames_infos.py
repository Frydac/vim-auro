from pathlib import Path
from pprint import pprint
from typing import List
from enum import Enum

Bt = Enum('BasenameTypeEnum', 'hpp cpp c h test asd')

basename_matchers = {
        Bt.hpp:  ['.hpp', '.hxx'], # cpp headers
        Bt.cpp:  ['.cpp'],         # cpp source
        Bt.h:    ['.h'],           # c headers
        Bt.c:    ['.c', '.cc'],    # c source
        Bt.test: ['_tests.cpp'],   # c and cpp test
        Bt.asd:  ['.asd']
        }


Dt = Enum('DirnametypeEnum', 'public protected private test_public test_protected test_private inc src test_inc test_src asd')

dirname_matchers = {
        Dt.public:         '{base_dir}/public/{namespace}',
        Dt.protected:      '{base_dir}/protected/{namespace}',
        Dt.private:        '{base_dir}/private/{namespace}',
        Dt.test_public:    '{base_dir}/test/public/{namespace}',
        Dt.test_protected: '{base_dir}/test/protected/{namespace}',
        Dt.test_private:   '{base_dir}/test/private/{namespace}',
        Dt.asd:   '{base_dir}/asd/{namespace}',

        Dt.inc:            '{base_dir}/inc/{namespace}',
        Dt.src:            '{base_dir}/src/{namespace}',
        Dt.test_inc:       '{base_dir}/test/inc/{namespace}',
        Dt.test_src:       '{base_dir}/test/src/{namespace}',
        }

related_header_info = {
        'basename_mapping': [{'from': [Bt.cpp, Bt.test, Bt.asd], 'to': [Bt.hpp, Bt.h]},
               {'from': [Bt.c],            'to': [Bt.h]}],

        'dirname_mapping': [{'from': [Dt.public, Dt.test_public, Dt.asd],       'to': [Dt.public]},
               {'from': [Dt.protected, Dt.test_protected, Dt.asd], 'to': [Dt.protected, Dt.public]},
               {'from': [Dt.private, Dt.asd],                      'to': [Dt.private, Dt.public]},
               {'from': [Dt.test_private, Dt.asd],                 'to': [Dt.private, Dt.protected, Dt.public]},

               {'from': [Dt.inc, Dt.test_inc, Dt.asd],             'to': [Dt.inc]},
               {'from': [Dt.src, Dt.test_src, Dt.asd],             'to': [Dt.src, Dt.inc]}],
        'basename_matchers': basename_matchers,
        'dirname_matchers': dirname_matchers
        }

related_source_info = {
        'basename_mapping':[{'from': [Bt.h, Bt.test, Bt.hpp], 'to': [Bt.cpp]},
              {'from': [Bt.h, Bt.test],         'to': [Bt.c]}],
        'dirname_mapping':[{'from': [Dt.public, Dt.test_public], 'to': [Dt.public, Dt.protected, Dt.private]},
              {'from': [Dt.protected],              'to': [Dt.protected]},
              {'from': [Dt.private],                'to': [Dt.private]},
              {'from': [Dt.test_private],           'to': [Dt.private, Dt.protected, Dt.public]},
              {'from': [Dt.test_protected],         'to': [Dt.protected, Dt.public]},

              {'from': [Dt.inc, Dt.test_inc],       'to': [Dt.inc, Dt.src]},
              {'from': [Dt.src, Dt.test_src],       'to': [Dt.src]}],
        'basename_matchers': basename_matchers,
        'dirname_matchers': dirname_matchers
        }

related_test_info = {
        'basename_mapping':[{'from': [Bt.h, Bt.hpp, Bt.c, Bt.cpp], 'to': [Bt.test]} ],
        'dirname_mapping':[{'from': [Dt.public],    'to': [Dt.test_public, Dt.test_private]},
              {'from': [Dt.protected], 'to': [Dt.test_protected]},
              {'from': [Dt.private],   'to': [Dt.test_private]},

              {'from': [Dt.inc],       'to': [Dt.test_inc, Dt.test_src]},
              {'from': [Dt.src],       'to': [Dt.test_src]}],
        'basename_matchers': basename_matchers,
        'dirname_matchers': dirname_matchers
        }

related_asd_info = {
        'basename_mapping':[{'from': [Bt.h, Bt.test, Bt.hpp], 'to': [Bt.asd]}],
        'dirname_mapping':[{'from': [Dt.public, Dt.protected, Dt.private], 'to': [Dt.asd]}],
        'basename_matchers': basename_matchers,
        'dirname_matchers': dirname_matchers
        }

related_header_info_from_asd = {
        'basename_mapping': [{'from': [Bt.asd],  'to' : [Bt.hpp, Bt.h]}],
        'dirname_mapping': [{'from': [Dt.asd],   'to' : [Dt.public, Dt.protected, Dt.private]}],
        'basename_matchers': basename_matchers,
        'dirname_matchers': dirname_matchers
        }

c_cpp_infos = [related_header_info, related_source_info, related_test_info, related_asd_info] 
asd_infos = [related_header_info_from_asd]

infos = {}
infos['c'] = c_cpp_infos
infos['cpp'] = c_cpp_infos
infos['tree'] = asd_infos
infos['asd'] = asd_infos
