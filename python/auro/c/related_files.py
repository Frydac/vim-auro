from pathlib import Path
from pprint import pprint
from auro.path import AuroPath, Ft
from typing import List

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
