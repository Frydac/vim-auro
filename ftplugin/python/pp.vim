nnoremap <buffer> <leader>pp viwyoprint("█<space><c-r>0:")<cr>pprint(<c-r>0)<esc>
vnoremap <buffer> <leader>pp <esc>oprint("█<space><c-r>*:")<cr>pprint(<c-r>*)<esc>

nnoremap <buffer> <leader>pli viwyologging.info("<c-r>0: %s", pformat(<c-r>0))<esc>
vnoremap <buffer> <leader>pli yologging.info("<c-r>0: %s", pformat(<c-r>0))<esc>
