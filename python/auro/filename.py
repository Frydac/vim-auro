from auro.related_filenames_infos import infos
from auro.dirname import Dirname, DirnameMatcher
from auro.basename import Basename, BasenameMatcher
from pathlib import PurePath
from auro.related_filenames import related_filenames_instantiated_matchers
from pprint import pprint
import os

# TODO: extend this wen needed, in context of vim the extension should alays be passed to Filename
def detect_ft(fn: str):
    ft_map = {
        "c": [".c", ".h"],
        "cpp": [".cpp", ".hpp"],
        "ruby": [".rb"],
        "python": [".py"]
    }
    _, ext = os.path.splitext(fn)
    for ft, exts in ft_map.items():
        for map_ext in exts:
            if map_ext == ext:
                return ft
    return None

related_info_map = {
        "header": 0,
        "source": 1,
        "test": 2,
        "asd": 3
        }

class Filename():
    def __init__(self, fn, ft=None):
        """
        @param ft Vim filetype (c, cpp, python, ruby, ..)
        """
        self.fn = fn
        self.filetype = ft
        if not self.filetype:
            self.filetype = detect_ft(fn)
        if not self.filetype:
            raise Exception("Don't detect filetype for {}".format(fn))
        if not self.filetype in infos.keys():
            raise Exception(
                "No path information specified for filetype '{}'".format(self.filetype))
        self.ft_info = infos[self.filetype]

        # TODO: we now take the the infos for key 2, but should be merged from
        # all available. Each info key can potentially have its own set of
        # basename/diraname matchers
        self.basename = Basename(self.ft_info[1]['basename_matchers'], fn)
        self.dirname = Dirname(self.ft_info[1]['dirname_matchers'], fn)

    def fn_include_no_ext(self):
        fn = ""
        if self.dirname.namespace:
            fn += self.dirname.namespace + "/"
        return (fn + self.basename.stem).replace('\\', '/')
        #  return str(Path(self.dirname.namespace) / self.basename.stem).replace('\\', '/')

    def fn_include(self):
        return self.fn_include_no_ext() + self.basename.ext

    def namespace_parts(self):
        if self.dirname.namespace:
            return PurePath(self.dirname.namespace).parts
        else:
            return ()

    def namespace(self):
        return self.dirname.namespace

    def classname(self):
        return self.basename.name

    def related_filenames(self, related_type: str):
        if not related_type in related_info_map.keys():
            raise Exception("{} not in related_info_map", format(related_type))
        related_info_ix = related_info_map[related_type]
        related_fns = related_filenames_instantiated_matchers(self.fn, self.ft_info[related_info_ix])
        return related_fns

    def existing_related_filenames(self, related_type: str):
        related_fns = self.related_filenames(related_type)
        existing_fns = []
        for fn in related_fns:
            if os.path.isfile(fn):
                existing_fns.append(fn)
        return existing_fns

    def has_single_existing_related_filename(self, related_type: str, ft: str):
        related_fns = self.existing_related_filenames(related_type)
        if (len(related_fns) == 1):
            if (Filename(related_fns[0]).filetype == ft):
                return True
        return False

    def __str__(self):
        result = ""
        result += "* fn: {}\n".format(self.fn)
        result += "* basename:\n{}\n".format(self.basename)
        result += "* dirname:\n{}\n".format(self.dirname)
        result += "* namespace: {}\n".format(self.namespace())
        return result

    def __repr__(self):
        return str(self)
