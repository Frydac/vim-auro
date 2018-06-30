from auro.python.related_files import related_filenames, related_test_info, related_source_info
from pprint import pprint
import unittest

class TestRelatedFilenames(unittest.TestCase):
    
    def test_related_filenames(self):

        #  print("█ related_test_info:")
        #  pprint(related_test_info)

        fn = '/home/emile/.vim/plugged/vim-auro/python/auro/python/related_files.py'
        print("█ fn:"); pprint(fn)
        fns_related = related_filenames(fn, related_test_info)
        print("fns_related:"); pprint(fns_related)
        self.assertEqual(fns_related, ['/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'])

        #  fn = '/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'
        #  print("█ fn:"); pprint(fn)
        #  fns_related = related_filenames(fn, related_test_info)
        #  print("fns_related:"); pprint(fns_related)
        #  self.assertEqual(fns_related, None)

        print("█ related_source_info:")
        pprint(related_source_info)

        #  fn = '/home/emile/.vim/plugged/vim-auro/python/auro/python/related_files.py'
        #  print("█ fn:"); pprint(fn)
        #  fns_related = related_filenames(fn, related_source_info)
        #  print("fns_related:"); pprint(fns_related)
        #  self.assertEqual(fns_related, None)

        fn = '/home/emile/.vim/plugged/vim-auro/python/test/auro/python/test_related_files.py'
        print("█ fn:"); pprint(fn)
        fns_related = related_filenames(fn, related_source_info)
        print("fns_related:"); pprint(fns_related)
        self.assertEqual(fns_related, ['/home/emile/.vim/plugged/vim-auro/python/auro/python/related_files.py'])

if __name__ == '__main__':
    unittest.main()
