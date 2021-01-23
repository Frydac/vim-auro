nnoremap <buffer> <leader>pp "zyiwostd::cout << "<c-r>z: " << <c-r>z << std::endl;<esc>
vnoremap <buffer> <leader>pp "zyostd::cout << "<c-r>z: " << <c-r>z << std::endl;<esc>

nnoremap <buffer> <leader>pd ^"zy$ostd::cout << "\|\| DEBUG: " << __FILE__ << ":" << __LINE__ - 1 << ": '<c-r>z'" << std::endl;<esc>
vnoremap <buffer> <leader>pd "zyostd::cout << "\|\| DEBUG: " << __FILE__ << ":" << __LINE__ - 1 << ": '<c-r>z'" << std::endl;<esc>

nnoremap <buffer> <leader>pl "zyiwolog_value("<c-r>z", <c-r>z);<esc>
