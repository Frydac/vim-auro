command! -buffer AuroHxx call c#auro_source_files#OpenHxxFile()
command! -buffer AuroCxx call c#auro_source_files#OpenCxxFile()
command! -buffer AuroTest call c#auro_source_files#OpenTestFile()

nnoremap <buffer> <silent> <leader>1 :AuroHxx<cr>
nnoremap <buffer> <silent> <leader>2 :AuroCxx<cr>
nnoremap <buffer> <silent> <leader>3 :AuroTest<cr>

"use for test
" nnoremap <buffer> <leader>4 :call c#auro_source_files#Test()<cr>
"calling non-existing function -> reload autoload buffer trick
" nnoremap <buffer> <leader>5 :silent! call c#auro_source_files#Reload()<cr>


