"For files like :
"path/core-dir/inc/dir/file.hpp
"path/core-dir/src/dir/file.cpp
"path/core-dir/test/dir/file_tests.cpp

" Create dictionary from filename with following keys:
" module = path to module name
" type = src, inc or test
" namespaces = array of dirs leading up to the filename e.g. ['auro', 'cx', 'v1']
" file = the filename without path
function! AuroSplit(fn)

    let l:result = {}
    let l:result.module = fnamemodify(a:fn, ':h') 
    let l:result.type = ""
    let l:result.namespaces = []
    let l:result.file = fnamemodify(a:fn, ':t:r')
    let l:result.ext = fnamemodify(a:fn, ':e')

    let l:stop_dirs = ['src', 'inc']

    while (index(l:stop_dirs, l:result.type) < 0)
        "we don't want the last value result.type will have in this loop, so we do it
        "before assigning the next dir name to it.
        if(l:result.type != "")
            let l:result.namespaces = add(l:result.namespaces, l:result.type)
        endif
        let l:result.type = fnamemodify(l:result.module, ':t')
        let l:result.module = fnamemodify(l:result.module, ':h')
    endwhile
    "we added them from back to front, so reverse
    call reverse(l:result.namespaces)
    "remove trailing /test if it exists
    if match(l:result.module, '/test') == len(l:result.module) - 5
        let l:result.module = l:result.module[:-5-1]
    endif
    return l:result
endfunction

"expand array of dir names to path
function! JoinDir(dir_array)
    let l:result = ""
    for dir in a:dir_array
        let l:result = l:result . '/' . dir
    endfor
    return l:result
endfunction

" return c or cpp
function! CxxExt(ext)
    return {'h': 'c', 'c': 'c', 'hpp': 'cpp', 'cpp': 'cpp'}[tolower(a:ext)]
endfunction

" return h or hpp
function! HxxExt(ext)
    return {'c': 'h', 'h': 'h', 'cpp': 'hpp', 'hpp': 'hpp'}[tolower(a:ext)]
endfunction


"There are 2 possible filenames for a header, in inc or src
"Presumes auro_split.ext = c or cpp
function! AuroHppNames(auro_split)
    let l:result = {'inc': '', 'src': ''}

    let l:ns_part = JoinDir(a:auro_split.namespaces)
    let l:h_ext = HxxExt(a:auro_split.ext)
    " common part for both inc and src
    let l:common = l:ns_part . '/' . a:auro_split.file . '.' . l:h_ext

    let l:result.inc = a:auro_split.module . '/inc' . l:common
    let l:result.src = a:auro_split.module . '/src' . l:common

    return l:result
endfunction


"Presumes auro_split.ext = h or hpp
function! AuroCppName(auro_split)
    let l:result = ''

    let l:c_ext = CxxExt(a:auro_split.ext)
    let l:ns_part = JoinDir(a:auro_split.namespaces)

    let l:result = a:auro_split.module . '/src' . l:ns_part . '/' . a:auro_split.file . '.' . l:c_ext

    return l:result
endfunction

"Removes the _tests from the file
function! AuroRemove_tests(file)
    let l:file = a:file
    let l:pos = match(l:file, "_tests" ) 
    let l:expected_pos = len(a:file) - 6
    if(l:pos == l:expected_pos)
        let l:file = l:file[:l:pos-1]
    endif
    return l:file
endfunction

"TODO: first find header file, than use that type
function! AuroTestCppName(auro_split)
    let l:ns_part = JoinDir(a:auro_split.namespaces)
    let l:result = a:auro_split.module . '/test/' . a:auro_split.type . l:ns_part . '/' . a:auro_split.file . '_tests.cpp'

    return l:result
endfunction

function! c#auro_source_files#Test()
    "let l:split = AuroSplit(expand('%'))
    "echom 'Module: ' . l:split.module . ' * Type: '. l:split.type . ' * namespaces: ' . l:split.namespaces[0] .  ' * File: ' . l:split.file . ' * Ext: ' . l:split.ext
    "let l:hpp_names = AuroHppNames(l:split)
    "echom 'hpp_inc: ' . l:hpp_names.inc . ' * hpp_src: ' . l:hpp_names.src
    "let l:test_name = AuroTestCppName(l:split)
    "echom 'test_name: ' . l:test_name

    let l:split = AuroSplit(expand('%'))
    let l:split.file = AuroRemove_tests(l:split.file)
    call PrintSplit(l:split)

endfunction

function! PrintSplit(split)
    echom 'module:' . a:split.module
    echom 'type:' . a:split.type
    for ns in a:split.namespaces
        echom 'namespace: ' . ns
    endfor
    echom 'file:' . a:split.file
    echom 'ext:' . a:split.ext

endfunction

function! OpenFile(file)
    execute ":e " . a:file
endfunction


function! OpenCxxFile(file)
    if(filereadable(a:file))
        Openfile(a:file)
    else
        if input(a:file . " does not exist, create? (y/n): ") == 'y'
            Openfile(a:file)
        endif
    endif
endfunction


function! OpenHxxFile(files)
    if(!filereadable(l:hpp_fns.inc) && !filereadable(l:hpp_fns.src))
        let l:result input("Following files do not exist:\ni: " . files.inc . "\ns: " . files.src . "\nCreate? (i/s/n): ")
        if l:result ==? 'i' 
            call OpenFile(a:files.inc)
        elseif l:result ==? 's'
            call OpenFile(a:files.src)
        endif
    elseif filereadable(l:hpp_fns.src)
        call OpenFile(a:files.src)
    elseif filereadable(l:hpp_fns.inc)
        call OpenFile(a:files.inc)
    endif

endfunction

function! c#auro_source_files#OpenTestFile()
    let l:split = AuroSplit(expand('%'))
    let l:split.file = AuroRemove_tests(l:split.file)
    "call PrintSplit(l:split)
    let l:test_fn = AuroTestCppName(l:split)
    call OpenCxxFile(l:test_fn)
endfunction

function! c#auro_source_files#OpenCxxFile()
    let l:split = AuroSplit(expand('%'))
    let l:split.file = AuroRemove_tests(l:split.file)
    "call PrintSplit(l:split)
    let l:cpp_fn = AuroCppName(l:split)
    call OpenCxxFile(l:cpp_fn)
endfunction

function! c#auro_source_files#OpenHxxFile()
    let l:split = AuroSplit(expand('%'))
    let l:split.file = AuroRemove_tests(l:split.file)
    "call PrintSplit(l:split)
    let l:hpp_fns = AuroHppNames(l:split)
    call OpenHxxFile(l:hpp_fns)
endfunction

function! AuroGoToHeader()
    let l:split = AuroSplit(expand('%'))

endfunction
