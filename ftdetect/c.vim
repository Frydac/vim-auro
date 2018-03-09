" by default vim sets .h files to filetype cpp, which does not work well for
" snippets and some of my plugin features
au BufNewFile,BufRead *.h set filetype=c
