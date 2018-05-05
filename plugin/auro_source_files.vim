
command! AuroChangeDirToSuperModule call auro_source_files#FindChanceDirToSuperModule()
command! AuroChangeDirToModule call auro_source_files#FindChangeDirToModule()

nnoremap <silent> <leader>as :AuroChangeDirToSuperModule<cr>
nnoremap <silent> <leader>am :AuroChangeDirToModule<cr>

" let g:auro_plugin_dir = get(g:, 'auro_plugin_dir', expand('%:p'))
let g:auro_plugin_dir = expand('<sfile>:p:h:h')

python3 << endpython

import vim
import sys
import os

sys.path.insert(0, os.path.join(vim.eval("g:auro_plugin_dir"), 'lib'))
from testing import hello 
from myvim.auro_source_files import c_headers, goto_includes

def test():
    hello()

    # print("hello world")
    # print(vim.command("echom expand('%')"))
    # print(vim.eval("g:auro_plugin_dir"))
    # print("buffer name")
    # print(vim.current.buffer.name)
    # c_headers(vim.current.buffer.name)
    goto_includes(vim.current.buffer.name)

endpython


nnoremap <leader>te :py3 test()<cr>
