# TODO: I think better design would be to have parse functions and parse
# objects/results, and not contain both in a class.

from pathlib import PurePath, Path
from enum import Enum
from pprint import pprint
import re


class DirnameMatcher:
    """
    Parses the dirname matcher input string into base_dir/dir_part/namespace
    """

    def __init__(self, dn_type: str, dn_type_expression: str):
        assert isinstance(dn_type, Enum)
        assert isinstance(dn_type_expression, str)
        self.dn_type = dn_type
        self.dn_type_expr = dn_type_expression
        self.dir_part = self.__parse_dir_part(self.dn_type_expr)

    def __parse_dir_part(self, dn_type_expr: str):
        matches = re.match(r"{base_dir}(?P<dir_part>.*){namespace}", dn_type_expr)
        if not matches:
            raise AssertionError(
                "Can't parse DirnameMatcher description: "
                + self.dn_type_expr
                + ", for dirtype: "
                + self.dn_type
            )
        return matches.group("dir_part")

    def __str__(self):
        result = ""
        result += "dn_type      : " + str(self.dn_type) + "\n"
        result += "dn_type_expr : " + self.dn_type_expr + "\n"
        result += "dir_part     : " + self.dir_part + "\n"
        return result

    def __repr__(self):
        return str(self)


# os.path.normpath doesn't work on the regex.
def normalize_path_for_regular_expression(path: str):
    return path.replace("\\", "/")


class DirnameMatch:
    """
    Parses a given path to base_dir/dir_part/namespace, for one instance of DirnameMatcher
    """

    def __init__(self, dn_matcher: DirnameMatcher, dir_name: str):
        dir_name = normalize_path_for_regular_expression(dir_name)
        assert isinstance(dn_matcher, DirnameMatcher)
        self.dn_matcher = dn_matcher
        self.base_dir = ""
        self.namespace = ""
        # for some reason following line breaks my highlighting
        #  bd_ns_re = r'(?P<base_dir>.*)' + re.escape(dn_matcher.dir_part) + r'(?P<namespace>.*)'
        test = re.escape(dn_matcher.dir_part.rstrip("/"))
        bd_ns_re = r"(?P<base_dir>.*)" + test + r"(/(?P<namespace>.*))?"
        bd_ns_matches = re.match(bd_ns_re, dir_name)
        if bd_ns_matches:
            if (bd_ns_matches.group("base_dir") is not None):
                self.base_dir = bd_ns_matches.group("base_dir")
            if (bd_ns_matches.group("namespace") is not None):
                self.namespace = bd_ns_matches.group("namespace")
            self.dir_part = dn_matcher.dir_part

        # TODO: make log of this?
        #  print("Matching \n dir_name: {}\n matcher: {}".format(dir_name, dn_matcher))
        #  if (self):
        #      print(" Match found:")
        #      print(self)
        #  else:
        #      print(" Not a match!\n")

    def __str__(self):
        result = ""
        result += "base_dir : " + self.base_dir + "\n"
        result += "dir_part : " + self.dir_part + "\n"
        result += "namespace: " + self.namespace + "\n"
        return result

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return bool(self.base_dir)


class Dirname:
    """
    Parses a given path to base_dir/dir_part/namespace, for a certain set of DirnameMatchers
    """

    def __init__(self, dirname_matchers, path=None):
        self.dirname = ""
        self.type = None
        self.base_dir = ""
        self.namespace = ""
        # dir_part = the part between base_dir and namespace
        self.dir_part = ""
        self.__dn_matchers = dirname_matchers
        if path:
            self.parse(path)

    def parse(self, path: str):
        dirname = str(Path(path).parent)
        self.dirname = dirname
        dirname_matches = []
        for dn_matcher in self.__dn_matchers:
            dm = DirnameMatch(dn_matcher, dirname)
            if dm:
                dirname_matches.append(dm)
        if not dirname_matches:
            raise Exception(
                #  "No dirname matches for path '{}' and matcher expressions: \n{}".format(
                #      path, self.__dn_matchers)
                # TODO: log to file
                "No dirname matches for path '{}'\n".format(path)
            )
        best_match = max(dirname_matches, key=lambda dm: len(dm.dir_part))
        self.type = best_match.dn_matcher.dn_type
        self.base_dir = best_match.base_dir
        self.namespace = best_match.namespace
        self.dir_part = best_match.dir_part

    def valid(self):
        return self.type != None

    def __str__(self):
        result = ""
        result += "type      : " + str(self.type) + "\n"
        result += "base_dir  : " + self.base_dir + "\n"
        result += "dir_part  : " + self.dir_part + "\n"
        result += "namespace : " + self.namespace
        return result

    def __repr__(self):
        return str(self)
