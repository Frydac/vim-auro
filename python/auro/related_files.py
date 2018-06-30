from auro.path import AuroPath
import re
from enum import Enum
from pprint import pprint

Ft = Enum('FileType', 'c_header c_source cpp_header cpp_source test')

filetypes = {
        Ft.c_header:   ('.h'),
        Ft.c_source:   ('.c'),
        Ft.cpp_header: ('.hpp', '.hxx'),
        Ft.test:       ('_tests.cpp'),
        Ft.cpp_source: ('.cpp', '.cc')
        }

Dt = Enum('DirType', 'private protected public test')

# a path can have more than one matching DirType
dirtypes = {
        Dt.public:    re.compile('\/public\/'),
        Dt.protected: re.compile('\/protected\/'),
        Dt.private:   re.compile('\/private\/'),
        Dt.test:      re.compile('\/test\/(protected|public|private)/')
        }

related_header_info = { 
        'select_filetype': [
            {'from': Ft.cpp_source, 'to': [Ft.cpp_header, Ft.c_header]},
            {'from': Ft.c_source,   'to': [Ft.c_header]},
            {'from': Ft.test,       'to': [Ft.cpp_header, Ft.c_header]}
        ],
        'select_dirtype': [
            {'from': Dt.public,    'to': [Dt.public]},
            {'from': Dt.protected, 'to': [Dt.protected, Dt.public]},
            {'from': Dt.private,   'to': [Dt.private, Dt.public]},
        ],
        'from_dirs': {**header_source_dirs, **test_dirs},
        'to_dirs': header_source_dirs,
        'filetypes': filetypes
    }

related_source_info = { 
        'select_filetype':[
            {'from': Ft.cpp_header, 'to': [Ft.cpp_source]},
            {'from': Ft.c_header,   'to': [Ft.c_source]},
            {'from': Ft.test,       'to': [Ft.cpp_source, Ft.c_source]}
        ],
        'select_dirtype': [
            {'from': Dt.public,    'to': [Dt.public, Dt.private]},
            {'from': Dt.protected, 'to': [Dt.protected]},
            {'from': Dt.private,   'to': [Dt.private, Dt.public]}
        ],
        'from_dirs': {**header_source_dirs, **test_dirs},
        'to_dirs': header_source_dirs,
        'filetypes': filetypes
    }

related_test_info = { 
        'select_filetype':[
            {'from': Ft.cpp_source, 'to': [Ft.test]},
            {'from': Ft.c_source,   'to': [Ft.test]}
        ],
        'select_dirtype': [
            {'from': Dt.public,    'to': [Dt.public, Dt.private]},
            {'from': Dt.protected, 'to': [Dt.protected, Dt.private]},
            {'from': Dt.private,   'to': [Dt.private, Dt.public]}
        ],
        'from_dirs': {**header_source_dirs},
        'to_dirs': test_dirs,
        'filetypes': filetypes
    }

def get_filetype(fn, filetypes):
    for ft, exts in filetypes.items():
        if fn.endswith(exts):
            return ft

def get_dirtype(path, dirtypes):



def related_file(fn, info):
    path = AuroPath(fn)
    print("█ path:")
    print(path)
    fn_ft = get_filetype(fn, info['filetypes'])
    print("█ fn_ft:")
    pprint(fn_ft)
    fn_dt = get_dirtype(path, info['from_dirs'])

