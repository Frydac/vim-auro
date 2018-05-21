import unittest
from pathlib import Path
from pprint import pprint

from auro.c.init import *

class TestInit(unittest.TestCase):
    def test_shift(self):
        text = "1\n2\n\naf;lsdkjaf\n"
        print("█ text:")
        print(shift(1, text))
        
        
    def test_include_guard(self):
        path = AuroPath("/home/emile/repos/fusion-avs/comp-avs/test/inc/auro/avs/v1/metadata/Generated.Meta-data_tests.h")
        print("█")
        print(init_snip(path))
        #  print(IncludeGuard.open(path))

        path = AuroPath("/home/emile/repos/fusion-avs/comp-avs/test/inc/auro/avs/v1/metadata/Generated.Meta-data_tests.c")
        print("█")
        print(init_snip(path))
        
        path = AuroPath("/home/emile/repos/fusion-avs/comp-avs/src/auro/avs/v1/metadata/Generated.Meta-data_tests.cpp")
        print("█")
        print(init_snip(path))

        path = Path("/home/emile/repos/fusion-avs/comp-avs/src/auro/avs/v1/metadata/Generated.Meta-data_tests.cpp")
        print(init_snip(AuroPath(path)))
        is_file = path.is_file()
        print("█ is_file:")
        pprint(is_file)

        path = Path("/home/emile/repos/fusion-avs/comp-avs/src/auro/avs/v1/metadata/Generated.Meta-data_tests.hpp")
        print(init_snip(AuroPath(path)))
        is_file = path.is_file()
        print("█ is_file:")
        pprint(is_file)
        
    
