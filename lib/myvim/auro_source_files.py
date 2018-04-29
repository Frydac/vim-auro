from auro_path import AuroPath, possible_headers
import vim

def c_headers(path):
    headers = possible_headers(AuroPath(path))
    print(str(headers))

def c_headers_cb():
    return c_headers(vim.current.buffer.name)
    
