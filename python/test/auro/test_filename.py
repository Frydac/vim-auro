import unittest
from pprint import pprint
from auro.filename import Filename


class TestFilename(unittest.TestCase):
    def test_tdd(self):
        #  fn_str = "/home/emile/repos/all/comp/headphones/test/protected/auro/headphones/v2/WIIR_tests.cpp"
        #  fn = Filename(fn_str)
        #  print("█ fn: {}".format(fn_str))
        #  pprint(fn)

        #  related_headers = fn.existing_related_filenames("header")
        #  print("█ related_headers:")
        #  pprint(related_headers)

        fn_str = "/home/emile/repos/all/cli/tools/ruby/dir/fingerprint.rb"
        print("██fn_str:")
        pprint(fn_str)
        fn = Filename(fn_str)
        print("█ fn:")
        pprint(fn)

        fn_str = "/home/emile/repos/all/cli/tools/ruby/fingerprint.rb"
        print("██fn_str:")
        pprint(fn_str)
        fn = Filename(fn_str)
        print("█ fn:")
        pprint(fn)

        fn_str = "/home/emile/repos/all/fusion/am4hp/story/am4hp106.rb"
        print("██ fn_str:")
        pprint(fn_str)
        fn = Filename(fn_str)
        print("█ fn:")
        pprint(fn)
        print("\n")

        print("█ fn.dirname.dir_part:")
        pprint(fn.dirname.dir_part)
        print("█ story in fn.dirname.dir_part:")
        test = "story" in fn.dirname.dir_part
        pprint(test)


        pass
