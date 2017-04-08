# Vim-Auro

Vim plugin with utilities specific to my work environment.

## Usage
### Jump to or create file
3 commands are defined, with 3 predefined shortcuts
* `:AuroHxx` or  
  `<leader>1`  
  open .h or .hpp file from corresponding .c, .cpp or \_tests.cpp file
* `:AuroCxx` or  
  `<leader>2`  
  open .c or .cpp file from corresponding .h, .hpp or \_tests.cpp file
* `:AuroTest` or  
  `<leader>3`  
  open \_tests.cpp file from corresponding .h, .hpp, .c or .cpp file

If the file the plugin wants to jump to doesn't exist, it will prompt you with the question if you would like to create it.

## Known issues
* Can't jump from a '...\_tests.cpp' file to corresponding .c or .h file

## Whishlist
* fix known issues
* when creating file
  * .h or .hpp: add include guards and namespaces.
  * .c or .cpp: include corresponding header, add namespaces.
  * ..\_tests.cpp: include corresponding header, include catch header, add namespaces.
* add option to open in new tab, split, vsplit
  * for split workaround: first open split (Ctrl-W v or Ctrl-W s), then use plugin
