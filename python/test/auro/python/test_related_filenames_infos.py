from auro.python.related_filenames_infos import infos
from auro.related_filenames import related_filenames
from pprint import pprint
import os
import unittest

class TestRelatedFilenames(unittest.TestCase):
    
    def test_related_filenames2(self):
        self.assertEqual(len(infos), 3)
        related_source_info = infos[1]
        related_test_info = infos[2]

        print("█ related_test_info:")
        pprint(related_test_info)

        fn = '/home/emile/.vim/plugged/vim-auro/python/auro/python/related_files.py'
        print("█ fn:"); pprint(fn)
        fns_related = related_filenames(fn, related_test_info)
        print("fns_related:"); pprint(fns_related)
        self.assertEqual(fns_related, [os.path.normpath('/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py')])

        fn = '/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'
        print("█ fn:"); pprint(fn)
        fns_related = related_filenames(fn, related_test_info)
        print("fns_related:"); pprint(fns_related)
        self.assertEqual(fns_related, [])

        print("█ related_source_info:")
        pprint(related_source_info)

        fn = '/home/emile/.vim/plugged/vim-auro/python/auro/python/related_files.py'
        print("█ fn:"); pprint(fn)
        fns_related = related_filenames(fn, related_source_info)
        print("fns_related:"); pprint(fns_related)
        self.assertEqual(fns_related, [])

        fn = '/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'
        print("█ fn:"); pprint(fn)
        fns_related = related_filenames(fn, related_source_info)
        print("fns_related:"); pprint(fns_related)
        self.assertEqual(fns_related, [os.path.normpath('/home/emile/.vim/plugged/vim-auro/python/auro/python/related_files.py')])

if __name__ == '__main__':
    unittest.main()
