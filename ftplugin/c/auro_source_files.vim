command! -buffer AuroHxx call c#auro_source_files#OpenHxxFile()
command! -buffer AuroCxx call c#auro_source_files#OpenCxxFile()
command! -buffer AuroTest call c#auro_source_files#OpenTestFile()
command! -buffer AuroImplHpp call c#auro_source_files#OpenImplHppFile()
command! -buffer AuroImplCpp call c#auro_source_files#OpenImplCppFile()
command! -buffer AuroImplTest call c#auro_source_files#OpenImplTestFile()
command! -buffer AuroFindCurrentFileIncludes call c#auro_source_files#FindCurrentFileIncludes()

" nnoremap <buffer> <silent> <leader>1 :AuroHxx<cr>
" nnoremap <buffer> <silent> <leader>2 :AuroCxx<cr>
" nnoremap <buffer> <silent> <leader>3 :AuroTest<cr>
" nnoremap <buffer> <silent> <leader>4 :AuroImplHpp<cr>
" nnoremap <buffer> <silent> <leader>5 :AuroImplCpp<cr>
" nnoremap <buffer> <silent> <leader>6 :AuroImplTest<cr>
" nnoremap <buffer> <silent> <leader>af :AuroFindCurrentFileIncludes<cr>
" nnoremap <silent><leader>ain :py3 goto_includes()<cr>
"
"use for test
" nnoremap <buffer> <leader>4 :call c#auro_source_files#Test()<cr>
"calling non-existing function -> reload autoload buffer trick
nnoremap <buffer> <leader>7 :silent! call c#auro_source_files#Reload()<cr>

python3 << endpython
import vim, sys, os
sys.path.insert(0, os.path.join(vim.eval("g:auro_plugin_dir"), 'lib'))
from auro.vim.c.related_files import goc_related_filename
endpython

nnoremap <buffer> <silent> <leader>1 :py3 goc_related_filename(1)<cr>
nnoremap <buffer> <silent> <leader>2 :py3 goc_related_filename(2)<cr>
nnoremap <buffer> <silent> <leader>3 :py3 goc_related_filename(3)<cr>

