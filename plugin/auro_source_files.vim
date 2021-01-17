let g:auro_plugin_dir = expand('<sfile>:p:h:h')

python3 << endpython
import vim
import sys
import os

sys.path.insert(0, os.path.join(vim.eval("g:auro_plugin_dir"), 'lib'))
from myvim.auro_source_files import goto_includes
# from pathlib import PurePath
sys.path.insert(0, os.path.join(vim.eval("g:auro_plugin_dir"), 'python'))
from auro.path import AuroPath
from auro.vim.chdir_to import chdir_to_module_dir, chdir_to_supermodule_dir, chdir_to_current_file_dir
from auro.vim.related_files import goc_related_filename
from auro.vim.depending_files import find_files_including
from auro.vim.plot import plot_naft_log_filename_csv
from auro.vim.filename import Filename

endpython

nnoremap <silent> <Plug>(auro_goc_related_filename_1) :py3 goc_related_filename(1)<cr>
nnoremap <silent> <Plug>(auro_goc_related_filename_2) :py3 goc_related_filename(2)<cr>
nnoremap <silent> <Plug>(auro_goc_related_filename_3) :py3 goc_related_filename(3)<cr>
nnoremap <silent> <Plug>(auro_goc_related_filename_4) :py3 goc_related_filename(4)<cr>

nnoremap <silent> <Plug>(auro_chdir_to_current_file_dir) :py3 chdir_to_current_file_dir()<cr>
nnoremap <silent> <Plug>(auro_chdir_to_supermodule_dir)  :py3 chdir_to_supermodule_dir()<cr>
nnoremap <silent> <Plug>(auro_chdir_to_module_dir)       :py3 chdir_to_module_dir()<cr>

nmap <silent> <leader>1 <Plug>(auro_goc_related_filename_1)
nmap <silent> <leader>2 <Plug>(auro_goc_related_filename_2)
nmap <silent> <leader>3 <Plug>(auro_goc_related_filename_3)
nmap <silent> <leader>4 <Plug>(auro_goc_related_filename_4)

nmap <silent><leader>ad <Plug>(auro_chdir_to_current_file_dir)
nmap <silent><leader>as <Plug>(auro_chdir_to_supermodule_dir)
nmap <silent><leader>am <Plug>(auro_chdir_to_module_dir)

nnoremap <silent><leader>ain :py3 goto_includes()<cr>
" nnoremap <silent><leader>pap :py3 print(AuroPath(vim.current.buffer.name))<cr>

nnoremap <silent> <leader>af :py3 find_files_including()<cr>

nnoremap <silent> <leader>ap :py3 plot_naft_log_filename_csv(is_new_plot=False)<cr>
nnoremap <silent> <leader>aap :py3 plot_naft_log_filename_csv(is_new_plot=True)<cr>

nnoremap <silent> <leader>ayi :py3 vim.command('let @"="#include <' + Filename().fn_include() + '>"')<cr>
