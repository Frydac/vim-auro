let g:clang_format_fallback_style='WebKit'

if has('win32')
    let s:clang_path = 'C:/Program Files (x86)/LLVM/share/clang/'
else
    let s:clang_path = '/usr/share/clang/'
endif

if has('python')
    let s:py_cmd = 'pyfile'
elseif has('python3')
    let s:py_cmd = 'py3file'
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
map <silent> <C-K> :execute g:clang_format_cmd<cr>
"Format from insert mode
imap <silent> <C-K> <c-o>:execute g:clang_format_cmd<cr>
"Format whole file
map <silent> <M-k> :call FormatFile()<cr>
