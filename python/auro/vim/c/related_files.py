from auro.c.related_filenames_infos import infos
from auro.path import AuroPath
from auro.related_filenames import related_filenames
from pathlib import PurePath
from pprint import pprint
import vim
import os.path

def goc_related_filename(key_nr):
    index = key_nr - 1
    print("Finding related headers")
    if len(infos) < index:
        print("* No info available for nr: " + nr)
    related_header_info = infos[index]
    fn_buffer = vim.current.buffer.name
    fns_related = related_filenames(fn_buffer, related_header_info)
    existing_fns_related = [fn_related for fn_related in fns_related if os.path.isfile(fn_related)]
    if len(existing_fns_related) == 1:
        vim.command("e " + existing_fns_related[0])
    elif len(existing_fns_related) == 0:
        print("No related file found. TODO: ask to create one of the following file(s)")  
        pprint(fns_related)
    else:
        print("More than one related file found. TODO: ask to open one of the existing")
        pprint(fns_related)

