import unittest
from pprint import pprint
from enum import Enum
from auro.path import AuroPath, include_path
from auro.related_files import related_file, related_header_info
from pprint import pprint

#  from pprint import pprint

class TestRelatedFiles(unittest.TestCase):
    
    def test_test(self):
        fn = '/home/emile/repos/toplevel-fusion/comp-avs/test/protected/auro/avs/v1/metadata/QuantizerPositionC_tests.cpp'
        related_file(fn, related_header_info)



if __name__ == '__main__':
    unittest.main()
