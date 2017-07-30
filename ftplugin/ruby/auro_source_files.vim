
"command! -buffer AuroOpenTestFile call :OpenRubyTestFileEmile()

nnoremap <buffer> <silent> <leader>1 :call ruby#auro_source_files#OpenRubySourceFile()<cr>
nnoremap <buffer> <silent> <leader>3 :call ruby#auro_source_files#OpenRubyTestFile()<cr>


nnoremap <buffer> <leader>7 :call ruby#auro_source_files#Reload()<cr>
