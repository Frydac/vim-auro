from auro.filename import Filename
import auro.ruby.init as init
from pprint import pprint
import unittest

class TestFilename(unittest.TestCase):
    def test_tdd(self):
        fn = '/home/emile/repos/all/comp/headphones/story/hp73.rb'
        fn = Filename(fn)
        result = init.snip_init_story(fn)

        fn = "/home/emile/repos/all/fusion/am4hp/qc/v4_parameter_smoothing.rb"
        fn = Filename(fn)
        result = init.snip_init_qc_register_block(fn)
        print("snip_init_qc_register_block:")
        print(result)
        result = init.snip_init_qc_register_class(fn)
        print("snip_init_qc_register_class:")
        print(result)
