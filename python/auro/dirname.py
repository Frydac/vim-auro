from pathlib import PurePath, Path
from enum import Enum
import re

class DirnameMatcher():
    def __init__(self, dn_type, dn_type_expression):
        assert isinstance(dn_type, Enum)
        assert isinstance(dn_type_expression, str)
        self.dn_type = dn_type
        self.dn_type_expr = dn_type_expression
        self.dir_part = self.__parse_dir_part(self.dn_type_expr)

    def __parse_dir_part(self, dn_type_expr):
        matches = re.match(r'{base_dir}(?P<dir_part>.*){namespace}', dn_type_expr)
        if not matches:
            raise AssertionError("Can't parse DirnameMatcher description: " + self.dn_type_expr + ", for dirtype: " + self.dn_type)
        return matches.group('dir_part')

    def __str__(self):
        result = ''
        result += 'dn_type      : ' + str(self.dn_type) + '\n'
        result += 'dn_type_expr : ' + self.dn_type_expr + '\n'
        result += 'dir_part     : ' + self.dir_part
        return result

    def __repr__(self):
        return str(self)

# os.path.normpath doesn't work on the regex.
def normalize_path_for_regular_expression(path):
    return path.replace("\\", "/")

class DirnameMatch():
    def __init__(self, dn_matcher, dir_name):
        dir_name = normalize_path_for_regular_expression(dir_name)
        assert isinstance(dn_matcher, DirnameMatcher)
        self.dn_matcher = dn_matcher
        self.base_dir = ''
        self.namespace = ''
        bd_ns_re = r'(?P<base_dir>.*)' + re.escape(dn_matcher.dir_part) + r'(?P<namespace>.*)'
        bd_ns_matches = re.match(bd_ns_re, dir_name)
        if bd_ns_matches:
            self.base_dir = bd_ns_matches.group('base_dir')
            self.namespace = bd_ns_matches.group('namespace')
            self.dir_part = dn_matcher.dir_part

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
        best_match = max(dirname_matches, key = lambda dm: len(dm.dir_part))
        self.type = best_match.dn_matcher.dn_type
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

