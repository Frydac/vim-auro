# Vim-Auro

Vim plugin with utilities specific to my work environment.

## Installation
* With Vundle add to your .vimrc:  
`Plugin 'Frydac/vim-auro'`  

* A folder with **UltiSnips** snippits is included, to make them work you'll need the [UltiSnips plugin](https://github.com/SirVer/ultisnips), and add something like the following to your .vimrc:
```
    if has('win32')
        let g:UltiSnipsSnippetsDir='~/vimfiles/bundle/vim-auro/UltiSnips'
    else
        let g:UltiSnipsSnippetsDir='~/.vim/bundle/vim-auro/UltiSnips'
    endif
```
By default UltiSnips uses Tab to trigger it, but in my setup this is already taken. I use the following adjustments:
```
    let g:UltiSnipsExpandTrigger="<c-j>"
    let g:UltiSnipsJumpForwardTrigger="<c-j>"
    let g:UltiSnipsJumpBackwardTrigger="<c-h>"
    " If you want :UltiSnipsEdit to split your window.
    let g:UltiSnipsEditSplit="vertical"
```

## Usage  
### Jump to or create file  
Commands and corresponding shortcuts are defined. 
By default `<leader>` is `\`, see `:h mapleader`
* `:AuroHxx` or  
  `<leader>1`  
  open .h or .hpp file from corresponding .c, .cpp or \_tests.cpp file
* `:AuroCxx` or  
  `<leader>2`  
  open .c or .cpp file from corresponding .h, .hpp or \_tests.cpp file
* `:AuroTest` or  
  `<leader>3`  
  open \_tests.cpp file from corresponding .h, .hpp, .c or .cpp file
* `:AuroImplHpp` or  
  `<leader>4`  
  open Impl.hpp file from corresponding .c, .cpp or \_tests.cpp file
* `:AuroImplCpp` or  
  `<leader>5`  
  open Impl.cpp file from corresponding .h, .hpp or \_tests.cpp file
* `:AuroImplTest` or  
  `<leader>6`  
  open Impl\_tests.cpp file from corresponding .h, .hpp, .c or .cpp file

When the file to jump to doesn't exist, a prompt will ask you if you want to create that file.

### Change CWD
  Remark: These only work for files in submodules, it parses the path and uses inc/ src/ test/ to orient itself. (could be made more robust to check for a .git folder).

* `<leader>as`  
  *auro supermodule*: change current working directory to that of the supermodule containing the current file.  

* `<leader>am`  
  *auro module*: change current working directory to that of the module containing the current file.  

### Find stuff
Same remark as in Change CWD.

* `<leader>af`  
  *auro find*: find all the files that include the current file.  
  This only works for files in submodules, and depends on the [ack vim-plugin][1]. The ack plugin is easier to use and much faster than
  vimgrep. Please take a look at the Keyboard Shortcuts on that page (e.g. use `q` to exit the quickfix window that will pop up).  
  This command will change the current working directory to that of the supermodule containing the current file.  
  
## Known issues
* Can't jump from a '\_tests.cpp' file to corresponding `.c` or .h file
* When header is in `inc` then it expects the `\_tests.cpp` file to be in `inc` as well (which you probably want most of the time)

## Whishlist
* fix known issues
* when creating file
  * .h or .hpp: add include guards and namespaces.
  * .c or .cpp: include corresponding header, add namespaces.
  * \_tests.cpp: include corresponding header, include catch header, add namespaces.
* add option to open in new tab, split, vsplit
  * for split workaround: first open split (Ctrl-W v or Ctrl-W s), then use plugin
* add docs for inside vim
* add functionality to run unittests inside vim with a command using vim's makeprg


[1]: https://github.com/mileszs/ack.vim 
