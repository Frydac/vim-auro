from auro_path import AuroPath, possible_headers, find_includes
import vim
from pprint import pprint

def c_headers(path):
    headers = possible_headers(AuroPath(path))
    print(str(headers))

def c_headers_cb():
    return c_headers(AuroPath(vim.current.buffer.name))
    
def goto_includes():
    includes = find_includes(AuroPath(vim.current.buffer.name))
    last_include_lineix = max(includes.keys())
    pprint(last_include_lineix)
    vim.command(":normal m'")
    vim.current.window.cursor = (last_include_lineix + 1, 0)
