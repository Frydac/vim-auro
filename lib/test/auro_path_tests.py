import unittest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auro_path import AuroPath, possible_related_header_fns
from enum import Enum
from pprint import pprint

class Types(Enum):
    CPP = 0

class TestAuroPath(unittest.TestCase):
    
    def test_test(self):
        #  self.assertEqual(Types.CPP, type)
        #  Animal = Enum('Animal', 'one two')
        #  animal = Animal.one
        #  self.assertEqual(animal, Animal.one)
        #  self.assertEqual('bla', 'abla')
        path = AuroPath('C:/git/fusion-avs/comp-avs/src/auro/avs/v1/metadata/functions.cpp')
        print(path)
        path = AuroPath('/home/emile/repos/fusion-avs/comp-avs/src/test/auro/avs/v1/metadata/functions_tests.cpp')
        print(path)
        path = AuroPath(os.path.abspath(__file__))
        print(path)
        path = AuroPath('/home/emile/repos/fusion-avs/comp-avs/src/auro/avs/v1/metadata/functions.cpp')
        print(path)
        print("█ possible_related_header_fns(path):")
        pprint(possible_related_header_fns(path))



if __name__ == '__main__':
    unittest.main()
