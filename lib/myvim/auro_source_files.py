from auro_path import AuroPath, possible_headers, find_include_lines
import vim

def c_headers(path):
    headers = possible_headers(AuroPath(path))
    print(str(headers))

def c_headers_cb():
    return c_headers(vim.current.buffer.name)

def goto_includes(path):
    if not path:
        path = vim.current.buffer.name
    path = AuroPath(path)
    find_include_lines(path)


