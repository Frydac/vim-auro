from auro.path import AuroPath
from enum import Enum
from itertools import product
from pathlib import PurePath, Path
from pprint import pprint
import os
import re

import itertools
def flatten(list_of_lists):
    return list(itertools.chain(*list_of_lists))

def related_filenames(path, info):
    basename_types = [BasenameType(key, value) for key, value in info['basename_types'].items()]
    dir_types = [Dirtype(key, value) for key, value in info['dir_types'].items()]

    from_basename = Basename(basename_types , path)
    from_dirname = Dirname(dir_types, path)

    to_basename_type_enums = flatten([from_to_pair['to'] for from_to_pair in info['bt'] if from_basename.type in from_to_pair['from']])
    to_basename_types = [bn_type for bn_type in basename_types if bn_type.type in to_basename_type_enums]
    to_basenames = [create_basename(from_basename, to_bt) for to_bt in to_basename_types]

    to_dirname_type_enums = flatten([from_to_pair['to'] for from_to_pair in info['dt'] if from_dirname.type in from_to_pair['from']])
    to_dirname_types = [dn_type for dn_type in dir_types if dn_type.type in to_dirname_type_enums]
    to_dirnames = [create_dirname(from_dirname, to_dt) for to_dt in to_dirname_types]

    related_filenames = [str(PurePath(dirname) / PurePath(basename)) for dirname, basename in list(product(to_dirnames, to_basenames))]
    return related_filenames
    
def related_filenames_old(path, info):
    basename_types = [BasenameType(key, value) for key, value in info['basename_types'].items()]
    dir_types = [Dirtype(key, value) for key, value in info['dir_types'].items()]

    from_basename = Basename(basename_types , path)
    from_dirname = Dirname(dir_types, path)
    if not is_valid_from_bt_dt(from_basename, from_dirname, info):
        return None
    
    to_basename_types = [bn_type for bn_type in basename_types if bn_type.type in info['to_bt']]
    to_basenames = [create_basename(from_basename, to_bt) for to_bt in to_basename_types]
    
    to_dirtypes = [dir_type for dir_type in dir_types if dir_type.type in info['to_dt']]
    to_dirnames = [create_dirname(from_dirname, to_dt) for to_dt in to_dirtypes]

    related_filenames = [str(PurePath(dirname) / PurePath(basename)) for dirname, basename in list(product(to_dirnames, to_basenames))]
    return related_filenames

class BasenameType():
    def __init__(self, bn_type, bn_type_str):
        assert isinstance(bn_type, Enum)
        self.type = bn_type
        self.type_str = bn_type_str
        self.prefix, self.suffix = self._parse_pre_and_suffix(self.type_str)

    @staticmethod
    def _parse_pre_and_suffix(type_str):
        assert isinstance(type_str, list)
        assert len(type_str) > 0
        for ts in type_str:
            bt_has_name_matches = re.match(r'(?P<prefix>.*){name}(?P<suffix>.*)', ts)
            if bt_has_name_matches:
                return bt_has_name_matches.group('prefix'), bt_has_name_matches.group('suffix')
        return '', type_str[0]

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
        self.type = None
        self.name = ''
        self.__basename_types = basename_types
        if path:
            self.parse(path)
    
    def parse(self, path):
        path = PurePath(path)
        basename_matches = []
        for bt in self.__basename_types:
            bm = BasenameMatch(bt, path.name)
            if bm:
                basename_matches.append(bm)
        # presuming the shortest name match is the actual name
        best_match = min(basename_matches, key = lambda bm: len(bm.name))
        self.type = best_match.type.type
        self.name = best_match.name

    def __str__(self):
        result = ''
        result += 'type : ' + str(self.type) + '\n'
        result += 'name : ' + self.name
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

    def __repr__(self):
        return str(self)

# os.path.normpath doesn't work on the regex.
def normalize_path_for_regular_expression(path):
    return path.replace("\\", "/")

class DirnameMatch():
    def __init__(self, dir_type, dir_name):
        dir_name = normalize_path_for_regular_expression(dir_name)
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
        self.type = None
        self.base_dir = ''
        self.namespace = ''
        # dir_part = the part between base_dir and namespace
        self.dir_part = ''
        self.__dir_types = dir_types
        if path:
            self.parse(path)

    def parse(self, path):
        dirname = str(Path(path).parent)
        dirname_matches = []
        for dt in self.__dir_types:
            dm = DirnameMatch(dt, dirname)
            if dm:
                dirname_matches.append(dm)
                #  self.types.append(dt.type)
        best_match = min(dirname_matches, key = lambda dm: len(dm.base_dir))
        self.type = best_match.type.type
        self.base_dir = best_match.base_dir
        self.namespace = best_match.namespace
        self.dir_part = best_match.dir_part

    def __str__(self):
        result = ''
        result += 'type      : ' + str(self.type) + '\n'
        result += 'base_dir  : ' + self.base_dir + '\n'
        result += 'dir_part  : ' + self.dir_part + '\n'
        result += 'namespace : ' + self.namespace
        return result

    def __repr__(self):
        return str(self)

def to_bt_for(from_bt, info):
    pass

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

