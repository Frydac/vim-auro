let g:clang_format_fallback_style='WebKit'
if !has('win32')
    noremap <C-K> :pyf /usr/share/clang/clang-format.py<cr>
    inoremap <C-K> <c-o>:pyf /usr/share/clang/clang-format.py<cr>
else
    noremap <C-K> :pyf C:/Program Files (x86)/LLVM/share/clang/clang-format.py<cr>
    inoremap <C-K><c-o>:pyf C:/Program Files (x86)/LLVM/share/clang/clang-format.py<cr>
endif

