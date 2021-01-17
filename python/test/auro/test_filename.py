import unittest
from pprint import pprint
from auro.filename import Filename


class TestFilename(unittest.TestCase):
    def test_tdd(self):
        fn_str = "/home/emile/repos/all/comp/headphones/test/protected/auro/headphones/v2/WIIR_tests.cpp"
        fn = Filename(fn_str)
        print("█ fn: {}".format(fn_str))
        pprint(fn)

        related_headers = fn.existing_related_filenames("header")
        print("█ related_headers:")
        pprint(related_headers)

        pass
