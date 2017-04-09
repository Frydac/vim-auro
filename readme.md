# Vim-Auro

Vim plugin with utilities specific to my work environment.

## Installation
* With Vundle add to your .vimrc:  
`Plugin 'Frydac/vim-auro'`  


## Usage  
### Jump to or create file  
3 commands are defined, with 3 predefined shortcuts.  
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

When the file to jump to doesn't exist, a prompt will ask you if you want to create that file.

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
