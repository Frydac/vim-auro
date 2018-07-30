from auro.related_filenames import related_filenames
from auro.c.related_filenames_infos import infos
import unittest
from pprint import pprint
import os

class TestRelatedFilenames(unittest.TestCase):

    def test_c_related_filenames(self):

        self.assertEqual(len(infos), 3)

        related_header_info = infos[0]
        related_source_info = infos[1]
        related_test_info = infos[2]

        print("█ related_header_info:")
        pprint(related_header_info)
        related_source_info

        fn = '/home/emile/repos/toplevel-fusion/comp-avs/test/protected/auro/avs/v1/metadata/QuantizerPositionC_tests.cpp'
        print("█ fn:"); pprint(fn)
        fns_related = related_filenames(fn, related_header_info)
        paths = ['/home/emile/repos/toplevel-fusion/comp-avs/test/public/auro/avs/v1/metadata/QuantizerPositionC.hpp',
                 '/home/emile/repos/toplevel-fusion/comp-avs/test/public/auro/avs/v1/metadata/QuantizerPositionC.h',
                 '/home/emile/repos/toplevel-fusion/comp-avs/test/protected/auro/avs/v1/metadata/QuantizerPositionC.hpp',
                 '/home/emile/repos/toplevel-fusion/comp-avs/test/protected/auro/avs/v1/metadata/QuantizerPositionC.h']
        paths = [os.path.normpath(path) for path in paths]
        self.assertEqual(fns_related, paths)

        print("█ related_source_info:")
        pprint(related_source_info)

        fn = '/home/emile/repos/toplevel-fusion/comp-avs/test/protected/auro/avs/v1/metadata/QuantizerPositionC_tests.cpp'
        fns_related = related_filenames(fn, related_source_info)
        print("█ fns_related:")
        pprint(fns_related)

        related_test_info
        print("█ related_test_info:")
        pprint(related_test_info)

        #  fn = '/home/emile/.vim/plugged/vim-auro/python/auro/python/related_files.py'
        #  print("█ fn:"); pprint(fn)
        #  fns_related = related_filenames(fn, related_test_info2)
        #  print("fns_related:"); pprint(fns_related)
        #  self.assertEqual(fns_related, ['/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'])

        #  fn = '/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'
        #  print("█ fn:"); pprint(fn)
        #  fns_related = related_filenames(fn, related_test_info2)
        #  print("fns_related:"); pprint(fns_related)
        #  self.assertEqual(fns_related, [])

if __name__ == '__main__':
    unittest.main()
