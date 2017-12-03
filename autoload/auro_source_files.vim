let s:root_dir = expand('<sfile>:p:h:h')

function! auro_source_files#FindChanceDirToSuperModule()
ruby << EOF
    root_dir = Vim::evaluate("s:root_dir")
    load File.join(root_dir, 'lib/vim_helpers.rb')

    MyVim::find_change_dir_to_supermodule(Vim)
EOF
endfunction

function! auro_source_files#FindChangeDirToModule()
ruby << EOF
    root_dir = Vim::evaluate("s:root_dir")
    load File.join(root_dir, 'lib/vim_helpers.rb')

    MyVim::find_change_dir_to_module(Vim)
EOF

endfunction

" function! c#auro_source_files#FindChangeDirToSuperModule()
"     let split = AuroSplit(expand('%:p'))
"     execute 'cd ' . fnamemodify(split.module, ':h')
"     pwd
" endfunction

" function! c#auro_source_files#FindChangeDirToModule()
"     let split = AuroSplit(expand('%:p'))
"     execute 'cd ' . split.module
"     pwd
" endfunction
