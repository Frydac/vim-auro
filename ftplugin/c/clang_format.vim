let g:clang_format_fallback_style='WebKit'

" potential solution:
" https://vim.fandom.com/wiki/Mapping_keys_in_Vim_-_Tutorial_(Part_2)#Supplying_a_count_to_a_map

if has('win32')
    let s:clang_path = 'C:/Program Files (x86)/LLVM/share/clang/'
    map <silent><buffer> <C-K> :py3f 'C:/Program Files (x86)/LLVM/share/clang/clang-format.py'<cr>
    imap <silent><buffer> <C-K> <c-o>:py3f 'C:/Program Files (x86)/LLVM/share/clang/clang-format.py'<cr>
elseif has ('macunix')
    let s:clang_path = '/usr/local/Cellar/clang-format/12.0.1/share/clang/'
    map <silent><buffer> <C-K> :py3f '/usr/local/Cellar/clang-format/12.0.1/share/clang/clang-format.py'<cr>
    imap <silent><buffer> <C-K> <c-o>:py3f '/usr/local/Cellar/clang-format/12.0.1/share/clang/clang-format.py'<cr>
else
    let s:clang_path = '/usr/share/clang/'
    " let s:clang_path = '/home/emile/temp/'
    map <silent><buffer> <C-K> :py3f /usr/share/clang/clang-format.py<cr>
    imap <silent><buffer> <C-K> <c-o>:py3f /usr/share/clang/clang-format.py<cr>
endif

if has('python')
    let s:py_cmd = 'pyfile '
elseif has('python3')
    let s:py_cmd = 'py3file '
else
    echom "No python detected, can't make mapping for clang-format"
    " Exit early
    finish
end

let g:clang_format_cmd = s:py_cmd . s:clang_path . 'clang-format.py'

function! FormatFile()
    " This is documented in the clang-format.py script
    let l:lines="all"
    execute g:clang_format_cmd
endfunction

"Format from normal or visiual mode
" map <silent> <C-K> <cmd>execute g:clang_format_cmd<cr>
"Format from insert mode
" imap <silent> <C-K> <c-o>:execute g:clang_format_cmd<cr>
"Format whole file
map <silent><buffer> <M-k> :call FormatFile()<cr>
