let g:clang_format_fallback_style='WebKit'
if !has('win32')
    noremap <C-K> :py3file /usr/share/clang/clang-format.py<cr>
    inoremap <C-K> <c-o>:py3file /usr/share/clang/clang-format.py<cr>
else
    noremap <C-K> :py3file C:/Program Files (x86)/LLVM/share/clang/clang-format.py<cr>
    inoremap <C-K><c-o>:py3file C:/Program Files (x86)/LLVM/share/clang/clang-format.py<cr>
endif

