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
from pathlib import PurePath
sys.path.insert(0, os.path.join(vim.eval("g:auro_plugin_dir"), 'python'))
from auro.path import AuroPath

def chdir_to_current_file_dir():
    path = PurePath(vim.current.buffer.name).parent
    vim.command('cd ' + str(path))
    print("pwd: " + str(path))
endpython

nnoremap <leader>ain :py3 goto_includes()<cr>
nnoremap <leader>pap :py3 print(AuroPath(vim.current.buffer.name))<cr>
nnoremap <silent> <leader>ad :py3 chdir_to_current_file_dir()<cr>
