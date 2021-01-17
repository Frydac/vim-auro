# Vim-Auro

Vim plugin with utilities specific to my work environment.

<!-- vim-markdown-toc GFM -->

* [Installation](#installation)
* [Setup](#setup)
    * [Enable snippets.](#enable-snippets)
    * [Enable finding of files that include this buffer](#enable-finding-of-files-that-include-this-buffer)
* [Features](#features)
* [Usage](#usage)
    * [Related filenames](#related-filenames)
    * [Change vim pwd](#change-vim-pwd)
    * [Find files including the current buffer](#find-files-including-the-current-buffer)
    * [Snippets](#snippets)
        * [filetype c and cpp](#filetype-c-and-cpp)
        * [filetype cpp](#filetype-cpp)
        * [filetype c](#filetype-c)

<!-- vim-markdown-toc -->


## Installation

* **Add plugin to your plugin manager.**  
  For example with [vim-plug](https://github.com/junegunn/vim-plug) add to your .vimrc:  
```
  Plug 'Frydac/vim-auro'
```

## Setup

### Enable snippets.
  A folder with **UltiSnips** snippits is included, to make them work you'll need the [UltiSnips plugin](https://github.com/SirVer/ultisnips), and add something like the following to your .vimrc:
```
    if has('win32')
        let g:UltiSnipsSnippetsDir='~/vimfiles/plugged/vim-auro/UltiSnips'
    else
        let g:UltiSnipsSnippetsDir='~/.vim/plugged/vim-auro/UltiSnips'
    endif
```
By default UltiSnips uses Tab to trigger it, but in my setup this is already taken. I use the following adjustments as suggested in the readme of UltiSnips:
```
    let g:UltiSnipsExpandTrigger="<c-j>"
    let g:UltiSnipsJumpForwardTrigger="<c-j>"
    let g:UltiSnipsJumpBackwardTrigger="<c-h>"
    " If you want :UltiSnipsEdit to split your window.
    let g:UltiSnipsEditSplit="vertical"
```

### Enable finding of files that include this buffer
  This feature depends on the [vim-ripgrep](https://github.com/jremmen/vim-ripgrep) plugin. 


## Features
  * **related filenames**: jump to or create related files quickly
  * **change vim pwd**: change the vim pwd to supermodule/module/current directory. Helpful for e.g. using grep like tools.
  * **find files including the current buffer**: defined for a few filetypes, uses [vim-ripgrep](https://github.com/jremmen/vim-ripgrep) to search for files including the current buffer.
  * **snippets**: a number of snippets are added, some are 'smart': they use the related filenames information to generate context aware snippets.

## Usage
Shortcut keys are predefined, some can be overridden if needed (see: `vim-auro/plugin/auro_source_files.vim`)  
By default `<leader>` is `\`, see `:h mapleader`  

### Related filenames
Currently related filename information is defined for filetypes: c, cpp, ruby, python.  
* `<leader>1`  
  c/cpp: open .h or .hpp file from corresponding .c, .cpp or \_tests.cpp file  
* `<leader>2`  
  c/cpp: open .c or .cpp file from corresponding .h, .hpp or \_tests.cpp file  
  python/ruby: open related source file from a corresponding test file
* `<leader>3`  
  c/cpp: open \_tests.cpp file from corresponding .h, .hpp, .c or .cpp file  
  python/ruby: open related test file from a corresponding source file
* `<leader>4`  
  c/cpp: open .asd file from corresponding .h file  

When the file to jump to doesn't exist, a prompt will ask you if you want to create that file.

### Change vim pwd
These work by running through the path of the current opened file and search for the .git file or folder.

* `<leader>as`  
  *auro supermodule*: change current working directory to that of the supermodule containing the current file. (by finding path with .git file/folder starting from left most parent folder)

* `<leader>am`  
  *auro module*: change current working directory to that of the module containing the current file. (by finding path with .git file/folder starting from right most parent folder) 

* `<leader>ad`  
  *auro directory*: change current working directory to that of the directory of the current file.

### Find files including the current buffer
Defined for filetypes c, cpp, ruby, python (not sure about python TODO review).  

* `<leader>af`  
  *auro find*: find all the files that include the current file.  
  Uses the related filenames information to parse the current path (namespace/classname) and construct a ripgrep search command using the `:Rg` command for the plugin [vim-ripgrep](https://github.com/jremmen/vim-ripgrep)  
  Note that the `:Rg` command uses the pwd to seach in.


### Snippets
  A number of snippets for the [UltiSnips plugin](https://github.com/SirVer/ultisnips) are defined. The code is currently a mess so its probably not easy to find where they are defined and needs to be reworked. I'll list a number fo them here per filetype.

#### filetype c and cpp

 * `init`   
   in a header will initialize the include guards, #ifdef __cplusplus, cpp namespace, and create a cpp class or c struct with the classname depending on the filename.
 * `ig`  
   *include guard* open and close
 * `igo`  
   *include guard* open
 * `crn`  
   *copy right notice*
  * `in`  
  *include*: when in the source: jump to last existing `#include` line and insert a new line starting with  
  `#include <{vector}>`
  * `ina`  
  *include auro*: when in the source: jump to last existing `#include` line and insert a new line starting with  
  `#include <auro/|>`
  * `inap`  
  *include auro path*: when in the source: jump to last existing `#include` line and insert a new line starting with  
  `#include <auro/ns1/ns2|>`  
   ns1 and ns2 are derived fromt he current buffer, so if you want to include something fromt he same directory)
  * `inh`  
  *include header*: useful in a .c or .cpp file to include corresponding header
  * `int`  
  *included test*: useful when in a _tests.cpp file to include both the header and the doctest.hpp header
  * `R`  
  `REQUIRE(){}`
  * `S`  
  `SECTION(){}`
  * `ui`, `cui`, `ul`, `ull`  
  `unsinged int`, `const unsigned int`, `unsigned long`, `unsigned long long`
  * `idcpp`  
  *if defined cpp*
  * `switch`  
  * `case`  
  * `main`  
  *main* function


#### filetype cpp
 * `usa`  
   *using namespace auro* add e.g. `using namespace auro::ns1::ns2;`. Usefull in `_tests.cpp` files
 * `nsa`  
   *namespace auro* add e.g. `namespace auro { namespace ns1 { namespace ns2 {  } } }`
 * `MS?S?`  
   matches to `M`, `MS` and `MSS` and expands to:  
   `MSS_BEGIN({bool}); MSS_END();`
  * `fora`, `forca`, `forcar`, `forar`, `fori`, `forui`  
  different for loop snippets, just try them out
  * `ca`  
  `const auto`
  * `un`  
  `using namespace`



#### filetype c
  * `c`  
   *c name* expands to e.g. `auro_ns1_ns1_ClassName_` Useful when working is C to type a little less
  * `cstr`  
   *c style struct*
  * `cenum`  
   *c style enum*
  * `cctor` `cctorb`  
   *c style constructor/destructor` pair (needs some work still)
  * `cf`  
   *c style 'member' function*
  * `afor`  
   *auro for*: expands on `AURO_FOR_BEGIN(...){...}AURO_FOR_END() `
  * `MS?S?R`  
   matches to `MR`, `MSR` and `MSSR` and expands to:  
   `MSS_BEGIN_RC({auro_ReturnCode_t}); MSS_END();`
  * `MS?S?B`  
   matches to `MB`, `MSB` and `MSSB` and expands to:  
   `MSS_BEGIN_B(); MSS_END_B();`
  


