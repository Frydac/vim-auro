nnoremap <buffer> <leader>pp viwyostd::cout << "<c-r>0: " << <c-r>0 << std::endl;<esc>
vnoremap <buffer> <leader>pp <esc>ostd::cout << "<c-r>*: " << <c-r>* << std::endl;<esc>

nnoremap <buffer> <leader>pl viwyolog_value("<c-r>0", <c-r>0);<esc>
