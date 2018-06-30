from enum import Enum
from itertools import product
from pathlib import PurePath, Path
from pprint import pprint
import re

Bt = Enum('BasenameType', 'source test')

basename_types = {
        Bt.source: '.py',
        Bt.test: 'test_{name}.py'
        }

Dt = Enum('DirType', 'source test')

dir_types = {
        Dt.source: '{base_dir}/python/{namespace}',
        Dt.test: '{base_dir}/python/test/{namespace}'
        }

related_source_info = {
        'from_bt':        [Bt.test],
        'from_dt':        [Dt.test],
        'to_bt':          [Bt.source],
        'to_dt':          [Dt.source],
        'basename_types': basename_types,
        'dir_types':      dir_types
        }

related_test_info = {
        'from_bt':        [Bt.source],
        'from_dt':        [Dt.source],
        'to_bt':          [Bt.test],
        'to_dt':          [Dt.test],
        'basename_types': basename_types,
        'dir_types':      dir_types
        }

class BasenameType():
    def __init__(self, bn_type, bn_type_str):
        assert isinstance(bn_type, Enum)
        self.type = bn_type
        self.type_str = bn_type_str
        self.prefix, self.suffix = self._parse_pre_and_suffix(self.type_str)

    @staticmethod
    def _parse_pre_and_suffix(type_str):
        bt_has_name_matches = re.match(r'(?P<prefix>.*){name}(?P<suffix>.*)', type_str)
        if bt_has_name_matches:
            return bt_has_name_matches.group('prefix'), bt_has_name_matches.group('suffix')
        else:
            return '', type_str

    def __str__(self):
        result = ''
        result += 'type     : ' + str(self.type) + '\n'
        result += 'type_str : ' + self.type_str + '\n'
        result += 'prefix   : ' + self.prefix + '\n'
        result += 'suffix   : ' + self.suffix
        return result

    def __repr__(self):
        return str(self)

class BasenameMatch():
    def __init__(self, bn_type, basename):
        assert isinstance(bn_type, BasenameType)
        self.type = bn_type
        self.basename = basename
        self.name = self.__parse_name(self.type, self.basename)

    @staticmethod
    def __parse_name(type, basename):
        name_re = re.escape(type.prefix) + '(?P<name>.*)' + re.escape(type.suffix)
        name_match = re.match(name_re, basename)
        if name_match:
            return name_match.group('name')

    def __bool__(self):
        return bool(self.name)

class Basename():
    def __init__(self, basename_types, path = None):
        self.types = []
        self.name = ''
        self.__basename_types = basename_types
        if path:
            self.process(path)
    
    def process(self, path):
        path = PurePath(path)
        basename_matches = []
        for bt in self.__basename_types:
            bm = BasenameMatch(bt, path.name)
            if bm:
                basename_matches.append(bm)
        # presuming the shortest name match is the actual name
        best_match = min(basename_matches, key = lambda bm: len(bm.name))
        self.types.append(best_match.type.type)
        self.name = best_match.name

    def __str__(self):
        result = ''
        result += 'types : ' + str(self.types) + '\n'
        result += 'name  : ' + self.name
        return result

    def __repr__(self):
        return str(self)

class Dirtype():
    def __init__(self, dir_type, dir_type_str):
        assert isinstance(dir_type, Enum)
        self.type = dir_type
        self.type_str = dir_type_str
        self.dir_part = self.__parse_dir_part(self.type_str)

    def __parse_dir_part(self, type_str):
        matches = re.match(r'{base_dir}(?P<dir_part>.*){namespace}', type_str)
        if not matches:
            raise AssertionError("Can't parse dirtype description: " + self.type_str + ", for dirtype: " + self.type)
        return matches.group('dir_part')

    def __str__(self):
        result = ''
        result += 'type     : ' + str(self.type) + '\n'
        result += 'type_str : ' + self.type_str + '\n'
        result += 'dir_part : ' + self.dir_part
        return result

class DirnameMatch():
    def __init__(self, dir_type, dir_name):
        assert isinstance(dir_type, Dirtype)
        self.type = dir_type
        self.base_dir = ''
        self.namespace = ''
        bd_ns_re = r'(?P<base_dir>.*)' + re.escape(dir_type.dir_part) + r'(?P<namespace>.*)'
        bd_ns_matches = re.match(bd_ns_re, dir_name)
        if bd_ns_matches:
            self.base_dir = bd_ns_matches.group('base_dir')
            self.namespace = bd_ns_matches.group('namespace')
            self.dir_part = dir_type.dir_part

    def __bool__(self):
        return bool(self.base_dir) and bool(self.namespace)

class Dirname():
    def __init__(self, dir_types, path = None):
        self.types = [] 
        self.base_dir = ''
        self.namespace = ''
        # dir_part = the part between base_dir and namespace
        self.dir_part = ''
        self.__dir_types = dir_types
        if path:
            self.process(path)

    def process(self, path):
        dirname = str(Path(path).parent)
        dirname_matches = []
        for dt in self.__dir_types:
            dm = DirnameMatch(dt, dirname)
            if dm:
                dirname_matches.append(dm)
                #  self.types.append(dt.type)
        best_match = min(dirname_matches, key = lambda dm: len(dm.namespace))
        self.types.append(best_match.type.type)
        self.base_dir = best_match.base_dir
        self.namespace = best_match.namespace
        self.dir_part = best_match.dir_part

    def __str__(self):
        result = ''
        result += 'types     : ' + str(self.types) + '\n'
        result += 'base_dir  : ' + self.base_dir + '\n'
        result += 'dir_part  : ' + self.dir_part + '\n'
        result += 'namespace : ' + self.namespace
        return result

def is_valid_from_bt_dt(basename, dirname, info):
    bt_matches = set(basename.types) == set(info['from_bt'])
    dt_matches = set(dirname.types) == set(info['from_dt'])
    return (bt_matches and dt_matches)

def create_dirname(dirname, dir_type):
    assert isinstance(dirname, Dirname)
    assert isinstance(dir_type, Dirtype)
    result = ''
    result += dirname.base_dir
    result += dir_type.dir_part
    result += dirname.namespace
    return result

def create_basename(basename, basename_type):
    assert isinstance(basename, Basename)
    assert isinstance(basename_type, BasenameType)
    result = ''
    result += basename_type.prefix
    result += basename.name
    result += basename_type.suffix
    return result

def related_filenames(path, info):
    basename_types = [BasenameType(key, value) for key, value in info['basename_types'].items()]
    basename = Basename(basename_types , path)
    dir_types = [Dirtype(key, value) for key, value in info['dir_types'].items()]
    dirname = Dirname(dir_types, path)

    if not is_valid_from_bt_dt(basename, dirname, info):
        return None
    
    to_basename_types = [bn_type for bn_type in basename_types if bn_type.type in info['to_bt']]
    to_basenames = [create_basename(basename, to_bt) for to_bt in to_basename_types]
    print("█ to_basenames:")
    pprint(to_basenames)
    
    to_dirtypes = [dir_type for dir_type in dir_types if dir_type.type in info['to_dt']]
    to_dirnames = [create_dirname(dirname, to_dt) for to_dt in to_dirtypes]
    print("█ to_dirnames:")
    pprint(to_dirnames)

    related_filenames = [str(PurePath(dirname) / PurePath(basename)) for dirname, basename in list(product(to_dirnames, to_basenames))]
    return related_filenames


