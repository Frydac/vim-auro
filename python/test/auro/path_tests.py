import unittest
from pprint import pprint
from enum import Enum
from auro.path import AuroPath, include_path

#  from pprint import pprint

class TestAuroPath(unittest.TestCase):
    
    def test_test(self):
        path = AuroPath('/home/emile/repos/fusion-avs/core-io/test/src/auro/src_code/generator/Generator_tests.cpp')
        print(path)
#          path = AuroPath('/home/emile/repos/fusion-avs/comp-avs/src/test/auro/avs/v1/metadata/functions_tests.cpp')
#          print(path)
#          path = AuroPath(os.path.abspath(__file__))
#          print(path)
#          path = AuroPath('/home/emile/repos/fusion-avs/comp-avs/src/auro/avs/v1/metadata/functions.cpp')
#          print(path)
#          print("█ possible_headers(path):")
#          pprint(possible_headers(path))
    
    def test_include_path(self):
        inc_path = include_path(AuroPath('/home/emile/repos/fusion-avs/core-io/src/auro/cli/args/formatter/Default.hpp'))
        print("█ inc_path:")
        pprint(inc_path)

if __name__ == '__main__':
    unittest.main()
