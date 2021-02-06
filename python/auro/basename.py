#TODO: see remark dirname.py

from pathlib import PurePath
from enum import Enum
from pprint import pprint
import re

#TODO: only uses the first match expression in the list, e.g. Bt.hpp: ['.hpp', '.hxx'] -> only .hpp is used
# solve with list of [prefix, suffix] pairs or something
class BasenameMatcher():
    """
    Holds and parses the user provided matcher for a certain basename type
    """
    def __init__(self, bn_type, bn_type_expressions):
        assert isinstance(bn_type, Enum)
        self.bn_type = bn_type
        self.bn_type_exprs = bn_type_expressions
        self.prefix, self.suffix = self._parse_pre_and_suffix(self.bn_type_exprs)

    @staticmethod
    def _parse_pre_and_suffix(bn_type_exprs):
        assert isinstance(bn_type_exprs, list)
        assert len(bn_type_exprs) > 0
        for bt_expr in bn_type_exprs:
            bt_expr_has_prefix = re.match(r'(?P<prefix>.*){name}(?P<suffix>.*)', bt_expr)
            if bt_expr_has_prefix:
                return bt_expr_has_prefix.group('prefix'), bt_expr_has_prefix.group('suffix')
        return '', bn_type_exprs[0]

    def __str__(self):
        result = ''
        result += 'bn_type       : ' + str(self.bn_type) + '\n'
        for bn_type_expr in self.bn_type_exprs:
            result += 'bn_type_expr : ' + bn_type_expr + '\n'
        result += 'prefix        : ' + self.prefix + '\n'
        result += 'suffix        : ' + self.suffix
        return result

    def __repr__(self):
        return str(self)

#TODO: only uses the first match expression in the list, e.g. Bt.hpp: ['.hpp', '.hxx'] -> only .hpp is used
class BasenameMatch():
    """
    Parses a given path to its bn_type and name, for one BasenameMatcher
    """
    def __init__(self, bn_matcher: BasenameMatcher, basename: str):
        assert isinstance(bn_matcher, BasenameMatcher)
        self.bn_matcher = bn_matcher
        self.basename = basename
        self.name = self.__parse_name(self.bn_matcher, self.basename)

    @staticmethod
    def __parse_name(bn_matcher, basename):
        name_re = re.escape(bn_matcher.prefix) + '(?P<name>.*)' + re.escape(bn_matcher.suffix) + '$'
        name_match = re.match(name_re, basename)
        if name_match:
            return name_match.group('name')

    def __bool__(self):
        return bool(self.name)

    def __str__(self):
        result = ''
        result += str(self.bn_matcher)
        return result

    def __repr__(self):
        return str(self)

class Basename():
    """
    Parses a given path to its bn_type and name, for a certain set of BasenameMatchers
    """
    def __init__(self, basename_matchers, path = None):
        assert all(isinstance(elem, BasenameMatcher) for elem in basename_matchers)
        self.type = None
        # name is what is left after basename matching
        self.name = ''
        # stem is the full basename without extension
        self.stem = ''
        # extension
        self.ext = ''
        self.__bn_matchers = basename_matchers
        if path:
            self.parse(path)
    
    def parse(self, path: PurePath):
        path = PurePath(path)
        self.stem = path.stem
        self.ext = path.suffix
        basename_matches = []
        for bn_matcher in self.__bn_matchers:
            bm = BasenameMatch(bn_matcher, path.name)
            if bm:
                basename_matches.append(bm)
        if not basename_matches:
            raise Exception(
                #  "No dirname matches for path '{}' and matcher expressions: \n{}".format(
                #      path, self.__bn_matchers
                # TODO: log to file
                "No basename matches for path basename '{}'\n".format(path.name)
            )
        # presuming the shortest name match is the actual name
        best_match = min(basename_matches, key = lambda bm: len(bm.name))
        self.type = best_match.bn_matcher.bn_type
        self.name = best_match.name

    def valid(self):
        return self.name != ''

    def __str__(self):
        result = ''
        result += 'type : ' + str(self.type) + '\n'
        result += 'name : ' + self.name
        return result

    def __repr__(self):
        return str(self)

