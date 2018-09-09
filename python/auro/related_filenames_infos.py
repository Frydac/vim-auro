# TODO: automatically find and source these files
# there should be a relation with the filename: use fn to get infos with function
# function should search path of filename for 

from auro.c.related_filenames_infos import infos as c_infos
from auro.ruby.related_filenames_infos import infos as ruby_infos
from auro.python.related_filenames_infos import infos as python_infos

infos = {**c_infos, **ruby_infos, **python_infos}

#  def get_info(fn):
    # use vim filetypedetect to get filetype for current file:
    # https://vi.stackexchange.com/questions/9962/get-filetype-by-extension-or-filename-in-vimscript
    # 
    #  pass

