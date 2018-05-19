from auro.path import AuroPath, include_path, filetype, Ft
from pathlib import PurePath
from auro.c.related_files import possible_headers
from auro.c.includes import find_includes, Type
from pprint import pprint
from typing import List

def _find_filetypes_of_included_header_to_test(path: AuroPath, vim_buffer: List[str]) -> List[Ft]:
    '''
    both .h and .hpp headers to test could be included in _tests.cpp, or None
    '''
    expected_possible_include_names = set([include_path(AuroPath(header)) for header in possible_headers(path)])
    vim_buffer_auro_includes = find_includes(vim_buffer)[Type.Auro]
    included_header_filetypes = []
    for vim_buffer_auro_include in vim_buffer_auro_includes:
        if (vim_buffer_auro_include.name in expected_possible_include_names):
            ft = filetype(vim_buffer_auro_include.name)
            if ft:
                included_header_filetypes.append(ft)
    return included_header_filetypes
    

def test_case_snip(path: AuroPath, vim_buffer: List[str]):
    included_header_filetypes = _find_filetypes_of_included_header_to_test(path, vim_buffer)
    if len(included_header_filetypes) == 1 and included_header_filetypes[0] == Ft.c:
        separator = "_"
    else:
        separator = "::"

    namespaces = path.namespaces[1:] if path.namespaces[0] == 'auro' else path.namespaces
    name = separator.join(path.namespaces)
    name += separator + path.classname
    tags = ''.join(["[%s]" % ns for ns in namespaces])
    snip_body = "TEST_CASE(\"test %s${1: }\", \"${2:[ut]}%s${3:[${4}]}\")\n" % (name, tags)
    snip_body += "{\n"
    snip_body += "    ${0}\n"
    snip_body += "}"
    return snip_body
