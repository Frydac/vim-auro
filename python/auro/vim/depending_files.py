from auro.dependening_files import rip_grep_cmd_files_including
from auro.vim.filename import Filename
import vim

def find_files_including(fn = None):
    "fn = None -> use current buffer"
    filename = Filename(fn)
    cmd = rip_grep_cmd_files_including(filename)
    print("Search command: {}".format(cmd))
    vim.command(cmd)
