let g:clang_format_fallback_style='WebKit'

if has('win32')
    let b:clang_path = 'C:/Program Files (x86)/LLVM/share/clang/'
else
    let b:clang_path = '/usr/share/clang/'
endif

if has('python')
    let b:pycmd = 'pyfile'
elseif has('python3')
    let b:pycmd = 'py3file'
else
    echom "No python detected, can't make mapping for clang-format"
    " Exit early
    finish
end

let b:clang_format_cmd = b:pycmd . b:clang_path . 'clang-format.py'

function! FormatFile()
    " This is documented in the clang-format.py script
    let l:lines="all"
    execute b:clang_format_cmd
endfunction

"Format from normal or visiual mode
map <silent> <C-K> :execute b:clang_format_cmd<cr>
"Format from insert mode
imap <silent> <C-K> <c-o>:execute b:clang_format_cmd<cr>
"Format whole file
map <silent> <M-k> :call FormatFile()<cr>
