import vim
from auro.related_filenames_infos import infos
from auro.vim.utils import vim_filetype
from pathlib import PurePath, Path
from auro.dirname import Dirname, DirnameMatcher
from auro.basename import Basename, BasenameMatcher
import vim

parsed_infos = {}
for ft, ft_info in infos.items():
    parsed_infos[ft] = [None] * len(ft_info)
    for ix, key_info in enumerate(ft_info):
        if not key_info:
            parsed_infos[ft][ix] = None
            continue
        parsed_infos[ft][ix] = {}
        parsed_infos[ft][ix]['basename_matchers'] = [BasenameMatcher(bn_type, bn_type_exprs) for bn_type, bn_type_exprs in infos[ft][ix]['basename_matchers'].items()]
        parsed_infos[ft][ix]['dirname_matchers'] = [DirnameMatcher(dn_type, dn_type_expr) for dn_type, dn_type_expr in infos[ft][ix]['dirname_matchers'].items()]


class Filename():
    """
    Uses the user provided basname and dirname info dictionaries to provide meta information about the given path.

    If constructed without fn -> vim.current.buffer is used and the vim_filetype is detected not only on filename extension

    TODO: this should be independent of vim?
    """
    def __init__(self, fn = None):
        self.filetype = vim_filetype(fn)
        if not fn:
            fn = vim.current.buffer.name
        if not self.filetype:
            raise Exception("Can't find vim filetype for {}".format(fn))
        if not self.filetype in parsed_infos.keys():
            raise Exception("No path information specified for filetype '{}'".format(self.filetype))
        self.ft_info = parsed_infos[self.filetype]
        if not self.ft_info:
            raise Exception("No info defined for fn with filetype {}".format(self.filetype))
        #TODO: we now take the the infos for key 2, but should be merged from all available
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

    def namespace_str(self):
        return self.dirname.namespace
