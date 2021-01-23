" Otherwise this is also executed for filetype='cpp'
if (&ft != 'c')
    finish
endif

for format in ['p', 'f', 'lf', 'u', 'lu', 'zu', 's']
    execute 'nnoremap <buffer> <leader>p' . format . ' "zyiwoprintf("<c-r>z: %' . format . '\n", <c-r>z);<esc>'
    execute 'vnoremap <buffer> <leader>p' . format . ' "zyoprintf("<c-r>z: %' . format . '\n", <c-r>z);<esc>'
endfor

" one special one we use 'i' for integer printing with format d, as we already
" use d for 'print debug' line
nnoremap <buffer> <leader>pi "zyiwoprintf("<c-r>z: %d\n", <c-r>z);<esc>
vnoremap <buffer> <leader>pi "zyoprintf("<c-r>z: %d\n", <c-r>z);<esc>

" print debug line
nnoremap <buffer> <leader>pd ^"zy$oprintf("\|\| DEBUG: %s:%d: '<c-r>z'\n", __FILE__, __LINE__ - 1);<esc>
vnoremap <buffer> <leader>pd "zyoprintf("\|\| DEBUG: %s:%d: '<c-r>z'\n", __FILE__, __LINE__ - 1);<esc>

