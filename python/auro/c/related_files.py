from pathlib import Path
from auro.path import AuroPath, Ft
from typing import List

def possible_headers(path: AuroPath) -> List[str]:
    if path.filetype not in [Ft.c, Ft.cpp]:
        return
    if not path.module:
        print("path doesn't have a module:")
        print(path)
        return
    possible_path_types = ['inc', 'src']
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

