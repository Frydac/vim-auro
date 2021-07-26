import unittest
from pprint import pprint
from auro.filename import Filename
from auro.gitdir import GitDir

def init_ruby_qc(fn):
    print("init_ruby_qc")
    result = "init_ruby_qc\n"
    indent = "    "
    super_module_dir = fn.git_modules()[0]["abs"]
    rel_dir = fn.path.parents[0].relative_to(super_module_dir)
    for part in rel_dir.parts:
        print("█ part:")
        pprint(part)


    result += fn.dirname.dir_part
    return result

class TestFilename(unittest.TestCase):
    def test_tdd(self):
        #  fn = "/home/emile/repos/all/cli/a3deng/qc"
        #  gitdir = GitDir(fn)

        fn = "/home/emile/repos/all/fusion/am4hp/qc/v4_parameter_smoothing.rb"
        init_ruby_qc(Filename(fn))


    
