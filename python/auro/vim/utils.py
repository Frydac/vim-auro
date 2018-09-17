import vim
from pathlib import PurePath
import re
from pprint import pprint

def vim_filetype(fn = None):
    """
    Try to parse and find the filetype that vim would assign based on file extension.
    Or get the current buffer's filetype, which is more robust.
    """

    if not fn:
        return vim.eval('&filetype')

    fn_ext = PurePath(fn).suffix[1:]
    filetypedetect = vim.eval('execute(\'autocmd filetypedetect\')')
    ft_re = re.compile(r'\s*\*\.(\S+)\s+setf\s+(\S+)')
    matching_filetypes = set()
    for line in filetypedetect.splitlines():
        md = ft_re.match(line)
        if not md:
            continue
        ext = md.group(1)
        if fn_ext != ext:
            continue
        ft = md.group(2)
        matching_filetypes.add(ft)
    if (len(matching_filetypes) == 1):
        return matching_filetypes.pop()
    elif (len(matching_filetypes) > 1):
        print("ERROR: multiple matching filetypes for: " + fn + ", filetypes: " + matching_filetypes)
    else:
        print("ERROR: cant find matching vim filetype for: " + fn)
        return None

