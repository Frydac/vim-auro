
# TODO: remove, to be deprecated, though need to replace usage with auro.vim.filename


from auro.dirname import Dirname, DirnameMatcher
from auro.basename import Basename
from auro.related_filenames_infos import infos
import os


class AuroPath2():
    def __init__(self, fn, basename_matchers, dirname_matchers):
        self.__bn_matchers = basename_matchers
        self.__dn_matchers = dirname_matchers
        self.init(fn)

    def init(self, fn):
        self.long_basename, self.ext = os.path.splitext(os.path.basename(fn))
        self.dirname = Dirname(self.__dn_matchers, fn)
        self.basename = Basename(self.__bn_matchers, fn)
        return self

    def fn_include_no_ext(self):
        print("█ basename:")
        pprint(self.basename)
        return str(Path(self.dirname.namespace) / self.basename.stem).replace('\\', '/')

    def fn_include(self):
        return self.fn_include_no_ext() + self.ext

# Below Deprecated, though might reuse parts ----------------------

from enum import Enum
from pathlib import PurePath, Path
from pprint import pprint
from typing import List, Optional
import re

Ft = Enum('FileType', 'cpp c ruby markdown python')
FtMap = {
        '.c': Ft.c, '.h': Ft.c,
        '.cpp': Ft.cpp, '.hpp': Ft.cpp,
        '.rb': Ft.ruby,
        '.py': Ft.python,
        '.md': Ft.markdown
        }

# TODO: use Basename/Dirname as basis
class AuroPath():
    """
    Extract metadata from paths organized the 'auro' way

    @param classname
      Usually the stem of the file, unless it ends with '_tests'.
    """

    __do_log = False

    def __init__(self, path_str):
        self.fn = Path(path_str)
        if self.__do_log:
            pprint(self.fn)
        self.module = None
        self.module_dir = None
        self.supermodule = None
        self.supermodule_dir = None
        self.types = []
        self.filetype = None
        self.classname = None
        self.namespaces = []
        self.__analyze_path(self.fn)

    Type = Enum('PathType', 'inc src test qc story script ruby lib python public private protected')

    def __str__(self):
        def nstr(s):
            return 'None' if s is None else str(s)
        result = ''
        result += 'fn              : ' + str(self.fn) + '\n'
        result += 'module          : ' + nstr(self.module) +  '\n'
        result += 'module_dir      : ' + nstr(self.module_dir) +  '\n'
        result += 'supermodule     : ' + nstr(self.supermodule) +  '\n'
        result += 'supermodule_dir : ' + nstr(self.supermodule_dir) +  '\n'
        result += 'types           : ' + str(self.types) + '\n'
        result += 'filetype        : ' + nstr(self.filetype) + '\n'
        result += 'classname       : ' + self.classname + '\n'
        result += 'namespaces      : ' + str(self.namespaces) + '\n'
        result += 'ext             : ' + str(self.ext) + '\n'
        return result

    def __analyze_path(self, path):
        self.ext = path.suffix
        self.__parse_filetype(path)
        self.__parse_classname(path)
        cur_path = Path('')
        for part in path.parts:
            cur_path /= part
            if self.__do_log: 
                print(cur_path)
            self.__parse_path_types(part, path)
            self.__parse_namespaces(self.types, part, path)
            self.__parse_git_modules(cur_path)

    def __parse_filetype(self, path):
        if path.suffix in FtMap:
            self.filetype = FtMap[path.suffix]

    def __parse_classname(self, path):
        self.classname = path.stem
        tests_suffix = '_tests'
        if self.classname.endswith(tests_suffix):
            self.classname = self.classname[:-len(tests_suffix)]

    def __parse_path_types(self, part, path):
        if str(part) in self.Type.__members__:
            self.types.append(self.Type[part])
            # makes this more robust should there have been a type in the path
            # that is not actually the type
            self.namespaces.clear()

    def __parse_namespaces(self, types, part, path):
        # the path types precede the first namespace part, and the last
        # part is the basename of the path
        if types and str(part) not in self.Type.__members__ and part != path.parts[-1]:
            self.namespaces.append(part)

    def __parse_git_modules(self, cur_path):
        if is_git_dir(cur_path):
            if not self.module:
                self.module_dir = str(cur_path)
                self.module = cur_path.name
            else:
                if not self.supermodule:
                    self.supermodule = self.module
                    self.supermodule_dir = self.module_dir
                self.module_dir = str(cur_path)
                self.module = cur_path.name
    
def is_git_dir(path):
    git_dir = Path(path) / '.git'
    return git_dir.exists()

def filetype(path: str) -> Optional[Ft]:
    ext = PurePath(path).suffix 
    if ext in FtMap:
        return FtMap[ext]
    return None

def include_path(path: AuroPath):
    result = ''
    if(path.namespaces):
        result = '/'.join(path.namespaces)
    result += '/' + path.classname
    result += path.ext
    return result
    
