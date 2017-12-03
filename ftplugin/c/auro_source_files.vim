command! -buffer AuroHxx call c#auro_source_files#OpenHxxFile()
command! -buffer AuroCxx call c#auro_source_files#OpenCxxFile()
command! -buffer AuroTest call c#auro_source_files#OpenTestFile()
command! -buffer AuroImplHpp call c#auro_source_files#OpenImplHppFile()
command! -buffer AuroImplCpp call c#auro_source_files#OpenImplCppFile()
command! -buffer AuroImplTest call c#auro_source_files#OpenImplTestFile()
command! -buffer AuroFindCurrentFileIncludes call c#auro_source_files#FindCurrentFileIncludes()

nnoremap <buffer> <silent> <leader>1 :AuroHxx<cr>
nnoremap <buffer> <silent> <leader>2 :AuroCxx<cr>
nnoremap <buffer> <silent> <leader>3 :AuroTest<cr>
nnoremap <buffer> <silent> <leader>4 :AuroImplHpp<cr>
nnoremap <buffer> <silent> <leader>5 :AuroImplCpp<cr>
nnoremap <buffer> <silent> <leader>6 :AuroImplTest<cr>
nnoremap <buffer> <silent> <leader>af :AuroFindCurrentFileIncludes<cr>

"use for test
" nnoremap <buffer> <leader>4 :call c#auro_source_files#Test()<cr>
"calling non-existing function -> reload autoload buffer trick
nnoremap <buffer> <leader>7 :silent! call c#auro_source_files#Reload()<cr>


