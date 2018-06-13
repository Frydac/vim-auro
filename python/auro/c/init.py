from auro.path import AuroPath, Ft, include_path
from auro.c.related_files import existing_related_header_fns
from pprint import pprint
import datetime
import re

class IncludeGuard:
    @staticmethod
    def name(path: AuroPath):
        result = "HEADER_"
        for ns in path.namespaces:
            result += ns + "_"
        result += path.classname + "_" + path.ext[1:]
        result = re.sub(r'[.-]', '_', result)
        result += "_ALREADY_INCLUDED"
        return result

    @staticmethod
    def open(path: AuroPath):
        ig_name = IncludeGuard.name(path)
        result = "#ifndef %s\n" % ig_name
        result += "#define %s" % ig_name
        return result

    @staticmethod
    def close():
        return '#endif'

class ExternC:
    @staticmethod
    def open():
        result = '#ifdef __cplusplus\n'
        result += 'extern "C" {\n'
        result += '#endif'
        return result

    @staticmethod
    def close():
        result = '#ifdef __cplusplus\n'
        result += '}\n'
        result += '#endif'
        return result

class Namespaces:
    nr_opened = 0

    @staticmethod
    def open(path: AuroPath):
        ns_snips = ["namespace %s{" % ns for ns in path.namespaces]
        result = ' '.join(ns_snips)
        Namespaces.nr_opened = len(path.namespaces)
        return result

    @staticmethod
    def close():
        result = ' '.join(['}' for i in range(Namespaces.nr_opened)])
        return result
        
def copyright_notice(path: AuroPath):
    file_name = include_path(path)
    year = datetime.datetime.now().year
    notice=u"""/*-------------------------------------------------------------------------
 * Name: {fn}
 *
 *  Copyright {y} Auro Technologies. All Rights Reserved. Auro-3D and 
 *  the related symbols are registered trademarks of Auro Technologies. 
 *  All materials and technology contained in this work are protected 
 *  by copyright law and may not be reproduced, distributed, transmitted, 
 *  displayed, published or broadcast, in whole or in part, without the 
 *  prior written permission of Auro Technologies NV or in the case of 
 *  third party materials, the owner of that content, file and/or method. 
 *  You may not alter or remove any trademark, copyright or other notice 
 *  from copies of the content, file and/or method. All other referenced 
 *  marks are those of their respective owners.
 *  
 *  Auro Technologies, phone +32-(0)-14314343, fax +32-(0)-14321224, 
 *  www.auro-technologies.com, info@auro-technologies.com.
 * 
 *-----------------------------------------------------------------------*/""".format(fn = file_name, y = year)
    return notice
    
def c_struct_snip(path: AuroPath):
    c_struct_name = '_'.join(path.namespaces)
    c_struct_name += "_%s_" % path.classname
    c_struct_name = re.sub(r'[.-]', '_', c_struct_name)
    snip_body = 'typedef struct ' + c_struct_name + '${1:Type}\n'
    snip_body += '{\n'
    snip_body += '    $0\n'
    snip_body += '} ' + c_struct_name + '$1t'
    return snip_body

def shift(level, text):
    shifted_text = ''
    # TODO: get correct shift width from vim/ultisnips
    tab = '    '
    for line in text.splitlines():
        if line:
            shifted_text += tab * level + line + '\n'
    return shifted_text

def class_snip(path: AuroPath):
    snip_body = 'class %s\n' % path.classname
    snip_body += '{\n'
    snip_body += 'public:\n'
    snip_body += '    $0\n'
    snip_body += 'private:\n'
    snip_body += '};'
    return snip_body

def c_related_header_include_snip(path: AuroPath):
    header_fns = existing_related_header_fns(path)
    snip_body = ""
    for header_fn in header_fns:
        inc_name = include_path(AuroPath(header_fn))
        snip_body += "#include \"%s\"\n" % inc_name
    return snip_body
    
def _init_c_header_snip(path: AuroPath):
    snip_body = ""
    snip_body += IncludeGuard.open(path) + '\n\n'
    if AuroPath.Type.inc in path.types:
        snip_body += copyright_notice(path) + '\n\n'
    snip_body += ExternC.open() + '\n\n'
    snip_body += c_struct_snip(path) + '\n\n'
    snip_body += ExternC.close() + '\n\n'
    snip_body += IncludeGuard.close() + '\n'
    return snip_body

def _init_c_source_snip(path: AuroPath):
    "includes all existing possible c headers"
    snip_body = ''
    snip_body += c_related_header_include_snip(path) + "\n"
    return snip_body

def _init_cpp_source_snip(path: AuroPath):
    "includes all existing possible headers, c an cpp"
    snip_body = ''
    snip_body += c_related_header_include_snip(path) + "\n"
    snip_body += Namespaces.open(path) + '\n\n'
    snip_body += '    $0\n\n'
    snip_body += Namespaces.close() + '\n'

    return snip_body

def _init_cpp_header_snip(path: AuroPath):
    snip_body = ""
    snip_body += IncludeGuard.open(path) + '\n\n'
    if AuroPath.Type.inc in path.types:
        snip_body += copyright_notice(path) + '\n\n'
    snip_body += Namespaces.open(path) + '\n\n'
    snip_body += shift(1, class_snip(path)) + '\n\n'
    snip_body += Namespaces.close() + '\n\n'
    snip_body += IncludeGuard.close() + '\n'
    return snip_body

def _init_cpp_test_source_snip(path: AuroPath):
    snip_body = 'to be implemented'
    return snip_body

def init_snip(path: AuroPath):
    "init snippet for c cpp h hpp test.cpp"
    assert(path.filetype == Ft.c or path.filetype == Ft.cpp)
    is_header = 'h' in path.ext
    print("█ path.filetype:")
    pprint(path.filetype)
    if path.filetype == Ft.c:
        if is_header:
            print('c_header')
            return _init_c_header_snip(path)
        else:
            print('c_source')
            return _init_c_source_snip(path)
    elif path.filetype == Ft.cpp:
        if is_header:
            print('cpp_header')
            return _init_cpp_header_snip(path)
        elif AuroPath.Type.test in path.types:
            print('cpp_test_source')
            return _init_cpp_test_source_snip(path)
        else:
            print('cpp_source')
            return _init_cpp_source_snip(path)
    else:
        raise AssertionError("filetype should not be handled by this function")

