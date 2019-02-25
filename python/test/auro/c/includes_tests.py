import unittest
from pprint import pprint

from auro.c.includes import *

class TestIncludes(unittest.TestCase):
    
    #  def test_some_stuff(self):
    #      include = Include();
    #      include.name = 'bla'
    #      print("█ include:")
    
    def test_find_includes(self):
        buff = ['#include <iostream>',
                '#include <auro/bla/file.cpp>',
                '#include <catch.hpp>']

        includes = find_includes(buff)

        self.assertEqual(len(includes[Type.Auro]), 1)
        self.assertEqual(includes[Type.Auro][0].name, 'auro/bla/file.cpp')

        expected_std_include = Include(name = 'iostream', line_nr = 0, line = '#include <iostream>')
        self.assertTrue(expected_std_include in includes[Type.Std])
    
    def test_find_include_guard(self):
        buff = """#ifndef HEADER_app_main_hpp_ALREADY_INCLUDED
#define HEADER_app_main_hpp_ALREADY_INCLUDED

#include "app/Options.hpp"
#include "app/json/Parser.hpp"
        """
        inc_guard = find_include_guard(buff.splitlines())
        print("█ inc_guard:")
        pprint(inc_guard)
        self.assertTrue(inc_guard)

        buff = """#ifndef HEADER_app_main_hpp_ALREADY_INCLUDED
#define ERROR_HEADER_app_main_hpp_ALREADY_INCLUDED

#include "app/Options.hpp"
#include "app/json/Parser.hpp"
        """
        inc_guard = find_include_guard(buff.splitlines())
        self.assertFalse(inc_guard)

if __name__ == '__main__':
    unittest.main()
