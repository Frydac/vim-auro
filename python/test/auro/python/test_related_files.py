import unittest
from pprint import pprint
from enum import Enum
from auro.path import AuroPath, include_path
#  from auro.related_files import related_file, related_header_info
from auro.python.related_files import related_filenames, related_test_info, related_source_info
from pprint import pprint

#  from pprint import pprint

class TestEmile(unittest.TestCase):
    
    def test_emile(self):

        print("█ related_test_info:")
        pprint(related_test_info)

        fn = '/home/emile/.vim/plugged/vim-auro/python/auro/python/related_files.py'
        print("█ fn:")
        pprint(fn)
        fns_related = related_filenames(fn, related_test_info)
        print("fns_related:")
        pprint(fns_related)

        fn = '/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'
        print("█ fn:")
        pprint(fn)
        fns_related = related_filenames(fn, related_test_info)
        print("fns_related:")
        pprint(fns_related)

        print("█ related_source_info:")
        pprint(related_source_info)

        fn = '/home/emile/.vim/plugged/vim-auro/python/auro/python/related_files.py'
        print("█ fn:")
        pprint(fn)
        fns_related = related_filenames(fn, related_source_info)
        print("fns_related:")
        pprint(fns_related)

        fn = '/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'
        print("█ fn:")
        pprint(fn)
        fns_related = related_filenames(fn, related_source_info)
        print("fns_related:")
        pprint(fns_related)

if __name__ == '__main__':
    unittest.main()
