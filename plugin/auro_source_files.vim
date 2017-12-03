
command! AuroChangeDirToSuperModule call auro_source_files#FindChanceDirToSuperModule()
command! AuroChangeDirToModule call auro_source_files#FindChangeDirToModule()

nnoremap <silent> <leader>as :AuroChangeDirToSuperModule<cr>
nnoremap <silent> <leader>am :AuroChangeDirToModule<cr>
