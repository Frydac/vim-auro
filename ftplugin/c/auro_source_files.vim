command! -buffer AuroHxx call c#auro_source_files#OpenHxxFile()
command! -buffer AuroCxx call c#auro_source_files#OpenCxxFile()
command! -buffer AuroTest call c#auro_source_files#OpenTestFile()

nnoremap <buffer> <leader>1 :AuroHxx<cr>
nnoremap <buffer> <leader>2 :AuroCxx<cr>
nnoremap <buffer> <leader>3 :AuroTest<cr>

"nnoremap <buffer> <leader>1 :call c#auro_source_files#OpenHxxFile()<cr>
"nnoremap <buffer> <leader>2 :call c#auro_source_files#OpenCxxFile()<cr>
"nnoremap <buffer> <leader>3 :call c#auro_source_files#OpenTestFile()<cr>

"nnoremap <buffer> <leader>4 :call c#auro_source_files#Test()<cr>

"nnoremap <buffer> <leader>5 :silent! call c#auro_source_files#Reload()<cr>


