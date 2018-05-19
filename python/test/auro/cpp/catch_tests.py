import unittest
from pprint import pprint

from auro.cpp.catch import *

class TestCatch(unittest.TestCase):
    
    def test_test_case_snip(self):
        
        vim_buffer = ["#include \"auro/avs/v1/metadata/GeneratedMetadata.h\""]
        path = AuroPath("/home/emile/repos/fusion-avs/comp-avs/test/src/auro/avs/v1/metadata/GeneratedMetadata_tests.cpp")
        print("█ path:")
        print(path)
        print(test_case_snip(path, vim_buffer))

        vim_buffer = ["#include \"auro/avs/v1/metadata/GeneratedMetadata.hpp\""]
        path = AuroPath("/home/emile/repos/fusion-avs/comp-avs/test/src/auro/avs/v1/metadata/GeneratedMetadata_tests.cpp")
        print(test_case_snip(path, vim_buffer))

        vim_buffer = ["#include \"auro/avs/v1/metadata/GeneratedMetadata.h\"", "#include \"auro/avs/v1/metadata/GeneratedMetadata.hpp\""]
        path = AuroPath("/home/emile/repos/fusion-avs/comp-avs/test/src/auro/avs/v1/metadata/GeneratedMetadata_tests.cpp")
        print(test_case_snip(path, vim_buffer))
