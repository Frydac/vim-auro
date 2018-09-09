from auro.basename import Basename
from auro.dirname import Dirname

class Filename:
    def __init__(self, fn_matchers, fn):
        self.dirname = Dirname(fn_matchers['dirname_matchers'], fn)
        self.basename = Basename(fn_matchers['basename_matchers'], fn)

    def include_path(self):
        "namespace + basename + [ext]"
        pass


