from pathlib import Path
from pprint import pprint
from auro.path import AuroPath, Ft
from typing import List

Bt = Enum('BasenameType', 'hpp cpp c h test')

basename_types = {
        Bt.hpp:  ['.hpp', '.hxx'],
        Bt.cpp:  ['.cpp'],
        Bt.h:    ['.h'],
        Bt.c:    ['.c', '.cc'],
        Bt.test: ['_tests.cpp']
        }

Dt = Enum('Dirtype', 'public protected private test_public test_protected test_private')

dir_types = {
        Dt.public:         '{base_dir}/public/{namespace}',
        Dt.protected:      '{base_dir}/protected/{namespace}',
        Dt.private:        '{base_dir}/private/{namespace}',
        Dt.test_public:    '{base_dir}/test/private/{namespace}',
        Dt.test_protected: '{base_dir}/test/protected/{namespace}',
        Dt.test_private:   '{base_dir}/test/private/{namespace}'
        }

related_header_info = [
        {
        'bt': [ {'from': [Bt.cpp, Bt.test], 'to': Bt.hpp},
                {'from': [Bt.c, Bt.test],   'to': Bt.h}]

        'dt': [ {'from': [Dt.public,    Dt.test_public],    'to': [Dt.public]},
                {'from': [Dt.protected, Dt.test_protected], 'to': [Dt.protected, Dt.public]},
                {'from': [Dt.private],     'to': [Dt.private, Dt.public]},
                {'from': [Dt.test_private, 'to': [Dt.private, Dt.protected, Dt.public]]}]
        'basename_types': basename_types,
        'dir_types': dir_types
        }]

related_source_info = [
        {
        'bt':[ {'from': [Bt.hpp, Bt.test], 'to': Bt.cpp},
               {'from': [Bt.h,   Bt.test], 'to': Bt.c}]
        'dt':[ {'from': [Dt.public, Dt.test_public], 'to': [Dt.public, Dt.protected, Dt.private]},
               {'from': [Dt.protected],        'to': [Dt.protected] },
               {'from': [Dt.private],          'to': [Dt.private]] },
               {'from': [test.test_private],   'to': [Dt.private,   Dt.protected, Dt.public]},
               {'from': [test.test_protected], 'to': [Dt.protected, Dt.public]}]
        'basename_types': basename_types,
        'dir_types': dir_types
        }]

related_test_info = [
        {
        'bt':[ {'from': [Bt.h, Bt.hpp, Bt.c, Bt.cpp], 'to': Bt.test} ]
        'dt':[ {'from': [Dt.public],    'to': [Dt.test_public, Dt.private]},
               {'from': [Dt.protected], 'to': [Dt.test_protected]},
               {'from': [Dt.private],   'to': [Dt.test_private]}]
        'basename_types': basename_types,
        'dir_types': dir_types
            }
        ]

def possible_related_header_fns(path: AuroPath) -> List[str]:
    if path.filetype not in [Ft.c, Ft.cpp]:
        return
    if not path.module:
        print("path doesn't have a git module: {}".format(path))
        return
    possible_path_types = ['inc']
    if AuroPath.Type.src in path.types:
        possible_path_types.append('src')
    possible_header_exts = {Ft.c: ['.h'], Ft.cpp: ['.h', '.hpp']}
    result = []
    for type in possible_path_types:
        for h_ext in possible_header_exts[path.filetype]:
            header_path = Path(path.module_dir)
            header_path /= type
            for ns in path.namespaces:
                header_path /= ns
            header_path /= path.classname + h_ext
            result.append(str(header_path))
    return result

def existing_related_header_fns(path: AuroPath):
    candidates = possible_related_header_fns(path)
    result = [fn for fn in candidates if Path(fn).is_file()]
    print("█ result:")
    pprint(result)
    return result

def possible_source_fns(path: AuroPath):
    pass

def possible_test_fns(path: AuroPath):
    pass
