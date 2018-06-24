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
from auro.vim.chdir_to import chdir_to_module_dir, chdir_to_supermodule_dir, chdir_to_current_file_dir

endpython

nnoremap <silent><leader>ain :py3 goto_includes()<cr>
nnoremap <silent><leader>pap :py3 print(AuroPath(vim.current.buffer.name))<cr>
nnoremap <silent><leader>ad :py3 chdir_to_current_file_dir()<cr>
nnoremap <silent><leader>as :py3 chdir_to_supermodule_dir()<cr>
nnoremap <silent><leader>am :py3 chdir_to_module_dir()<cr>
