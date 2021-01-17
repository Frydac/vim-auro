# TODO: automatically find and source these files
# there should be a relation with the filename: use fn to get infos with function
# function should search path of filename for 

from auro.c.related_filenames_infos import infos as c_infos
from auro.ruby.related_filenames_infos import infos as ruby_infos
from auro.python.related_filenames_infos import infos as python_infos

from auro.dirname import DirnameMatcher
from auro.basename import BasenameMatcher
from pprint import pprint

infos = {**c_infos, **ruby_infos, **python_infos}

def instantiate_matchers_from_description(key_info):
        if not key_info:
            # could be nothing
            return
        if not isinstance(key_info['basename_matchers'], list):
            # e.g. c and cpp filetypes have the same basename_matchers descriptions, can't instantiate 2x
            key_info['basename_matchers'] = [BasenameMatcher(bn_type, bn_type_exprs) for bn_type, bn_type_exprs in key_info['basename_matchers'].items()]
        if not isinstance(key_info['dirname_matchers'], list):
            key_info['dirname_matchers'] = [DirnameMatcher(dn_type, dn_type_expr) for dn_type, dn_type_expr in key_info['dirname_matchers'].items()]

# Prepare the matcher objects
for ft, ft_infos in infos.items():
    for ix, key_info in enumerate(ft_infos):
        instantiate_matchers_from_description(key_info)

#  def get_info(fn):
    # use vim filetypedetect to get filetype for current file:
    # https://vi.stackexchange.com/questions/9962/get-filetype-by-extension-or-filename-in-vimscript
    # 
    #  pass

