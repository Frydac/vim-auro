# Vim-Auro

Vim plugin with utilities specific to my work environment.

<!-- vim-markdown-toc GFM -->

* [Installation](#installation)
* [Dependencies and setup](#dependencies-and-setup)
    * [UltiSnips](#ultisnips)
    * [vim-ripgrep](#vim-ripgrep)
* [Features and Usage](#features-and-usage)
    * [Related filenames](#related-filenames)
    * [Change vim current working directory `:pwd`](#change-vim-current-working-directory-pwd)
    * [Find files including the current buffer](#find-files-including-the-current-buffer)
    * [Snippets](#snippets)
        * [filetype c and cpp](#filetype-c-and-cpp)
        * [filetype cpp](#filetype-cpp)
        * [filetype c](#filetype-c)
    * [Generate debug print statements](#generate-debug-print-statements)
        * [Cpp](#cpp)
        * [C](#c)
        * [Ruby](#ruby)
        * [Python](#python)
    * [Miscellaneous](#miscellaneous)
        * [Copy full path of current buffer into clipboard](#copy-full-path-of-current-buffer-into-clipboard)
        * [C/Cpp put include statement for current file into yank register](#ccpp-put-include-statement-for-current-file-into-yank-register)

<!-- vim-markdown-toc -->


## Installation

* **Add plugin to your plugin manager.**  
  For example with [vim-plug](https://github.com/junegunn/vim-plug) add to your .vimrc:  
```
  Plug 'Frydac/vim-auro'
```

## Dependencies and setup

### UltiSnips
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

### vim-ripgrep
  The [vim-ripgrep plugin](https://github.com/jremmen/vim-ripgrep) is used to [find files including the current buffer](#find-files-including-the-current-buffer).


## Features and Usage

Shortcut keys are predefined, some can be overridden if needed (see: `vim-auro/plugin/auro_source_files.vim`)  
By default `<leader>` is `\`, see `:h mapleader`  

### Related filenames
**Jump to or create related files quickly**  

Related filename information is defined for filetypes: c, cpp, ruby, python.  

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
Note: These depend on a description of the path and basename, so only works for files that match this description.  
TODO: Need to add just jumping between files in the same directory if the full path doesn't match any in the description. Useful when browsing an external code tree without our path conventions.

### Change vim current working directory `:pwd`
**Change the vim working directory `:pwd` to supermodule/module/current directory.**  

Helpful for e.g. using grep like tools.  

* `<leader>as`  
  *auro supermodule*: change current working directory to that of the supermodule containing the current file.  
  By finding path with .git file/folder starting from left most parent folder.

* `<leader>am`  
  *auro module*: change current working directory to that of the module containing the current file.  
  By finding path with .git file/folder starting from right most parent folder.

* `<leader>ad`  
  *auro directory*: change current working directory to that of the directory of the current file.

### Find files including the current buffer
Defined for filetypes c, cpp, ruby, python (not sure about python TODO review).  

* `<leader>af`  
  *auro find*: find all the files that include the current file.  
  Uses the related filenames information to parse the current path (namespace/classname) and construct a ripgrep search command using the `:Rg` command for the plugin [vim-ripgrep](https://github.com/jremmen/vim-ripgrep)  
  Note that the `:Rg` command uses the vim current working directory to search in.


### Snippets
  A number of snippets for the [UltiSnips plugin](https://github.com/SirVer/ultisnips) are defined. 
  Some of these are 'smart' as they use the related filename info to generate context aware content.  

  Note: The code is currently a mess so its probably not easy to find where they are defined and needs to be reworked. I'll list a number fo them here per filetype.

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

### Generate debug print statements

I've added some keymappings that generate debug print statements, printing the
variable under the cursor/selection, or printing the current line and number.

Notes:

* I've used 'non-configurable' keymaps, if these clash for you, please let me know, I can make the configurable (or make a pullrequest of course ). 
* They used to depend on the ['selection register'](https://vimhelp.org/change.txt.html#%7Bregister%7D) `*`, which didn't always work in all combos of vim/nvim/terminal/OS/clipboard, so now I yank them in register named `z` (which is just a register you are unlikely to use).

#### Cpp

* `<leader>pp`  
  When cursor on a `word` or using the visual selection, generate:  
  ```cpp
  std::cout << "word: " << word << std::endl;
  ```

* `<leader>pd`  
  *Print Debug*: Creates a new line under the current line/selection as follows:  
  ```cpp
  std::cout << "|| DEBUG: " << __FILE__ << ":" << __LINE__ - 1 << ": '<previous line/selection as string>'" << std::endl;  
  ```
  This is handy to know where the program is crashing, e.g. 'What line is causing the segfault?'

#### C

C doesn't have function overloads/templates.. \*shaking my head\*, so we need to specify the type.  
Currently there are multiple mappings defined for key/format ['p', 'f', 'lf', 'u', 'lu', 'zu', 's'],  
I'll give one example with 'f':  

* `<leader>pf`  
  When cursor on a `word` or using the visual selection, generate:  
  ```c
  printf("word: %f\n", word);
  ```
For printing integers I defined `<leader>pi` to print with format `%d` because `<leader>pd` is used for printing the debug statement.
  
* `<leader>pd`  
  *Print Debug*: Creates a new line under the current line/selection as follows:  
  ```c
  std::cout << "|| DEBUG: " << __FILE__ << ":" << __LINE__ - 1 << ": '<previous line/selection as string>'" << std::endl;  
  ```
  This is handy to know where the program is crashing, e.g. 'What line is causing the segfault?'

#### Ruby

* `<leader>pp`  
  *Print useing pretty printer*: When cursor on a `word` or using the visual selection, generate:
  ```ruby
  puts "█ word:"; pp word
  ```
  Which prints the content of word with `pp` which is best for hashes and bigger types, for single basic types maybe use the following.

* `<leader>`pr  
  *pr as in print*: When cursor on a `word` or using the visual selection, generate:
  ```ruby
  puts "█ word: #{word}"
  ```

#### Python

* `<leader>pp`  
  *Print useing pretty printer*: When cursor on a `word` or using the visual selection, generate:
  ```python
  print("█ word:")
  pprint(word)
  ```
  Which prints the content of word with `pprint` which is best for hashes and bigger types, for single basic types maybe use the following.
  Note: use the `pp` snippet to generate the import statement.

* `<leader>`pr  
  *pr as in print*: When cursor on a `word` or using the visual selection, generate:
  ```python
  print("█ word: {}".format(word))
  ```

### Miscellaneous

#### Copy full path of current buffer into clipboard

* `<leader>ayf`  
  *auro yank filename*  
  Yanks into the `+` vim register, this connects to the system clipboard if configured properly.  
  FYI: to paste in vim from this register, in normal mode do `"+p`, in insert mode do `<ctrl-r>+`

#### C/Cpp put include statement for current file into yank register

* `<leader>ayi`  
 *auro yank include*  
  Uses the related filename information to parse namespace/classname and populates the yank `"` (default) register, you can then paste it by pressing `p` in the file/line where you want to add the include.  
  I use this a lot when I don't know the exact path of the file I want to include, I use fzf to search for it and I open that buffer, then I use this keymap to generate/yank the include statement, jump back to the previous file (alternate buffer with `<ctrl-6>`) and paste it where it needs to go.

