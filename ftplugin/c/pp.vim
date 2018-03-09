if (&ft != 'c')
    finish
endif

nnoremap <buffer> <leader>pp viwyoprintf("<c-r>0: %d", <c-r>0);<esc>
vnoremap <buffer> <leader>pp <esc>oprintf("<c-r>*: %d", <c-r>*);<esc>

