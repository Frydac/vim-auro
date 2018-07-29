from auro.python.related_files import related_filenames, related_filenames2
from auro.c.related_files import related_header_info, related_source_info, related_test_info
import unittest
from pprint import pprint

class TestRelatedFilenames(unittest.TestCase):

    def test_c_related_filenames(self):

        print("█ related_header_info:")
        pprint(related_header_info)
        related_source_info

        fn = '/home/emile/repos/toplevel-fusion/comp-avs/test/protected/auro/avs/v1/metadata/QuantizerPositionC_tests.cpp'
        print("█ fn:"); pprint(fn)
        fns_related = related_filenames2(fn, related_header_info)
        print("█ fns_related:"); pprint(fns_related)

        print("█ related_source_info:")
        pprint(related_source_info)
        related_test_info
        print("█ related_test_info:")
        pprint(related_test_info)

        #  fn = '/home/emile/.vim/plugged/vim-auro/python/auro/python/related_files.py'
        #  print("█ fn:"); pprint(fn)
        #  fns_related = related_filenames2(fn, related_test_info2)
        #  print("fns_related:"); pprint(fns_related)
        #  self.assertEqual(fns_related, ['/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'])

        #  fn = '/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'
        #  print("█ fn:"); pprint(fn)
        #  fns_related = related_filenames2(fn, related_test_info2)
        #  print("fns_related:"); pprint(fns_related)
        #  self.assertEqual(fns_related, [])

if __name__ == '__main__':
    unittest.main()
