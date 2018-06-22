
function! c#auro_source_files#OpenTestFile()
    let split = AuroSplit(expand('%:p'))
    let test_fn = AuroTestCppName(split)
    call OpenOrCreateSingleFile(test_fn)
endfunction

function! c#auro_source_files#OpenCxxFile()
    let split = AuroSplit(expand('%:p'))
    let cpp_fn = AuroCppName(split)
    call OpenOrCreateSingleFile(cpp_fn)
endfunction

function! c#auro_source_files#OpenHxxFile()
    let split = AuroSplit(expand('%:p'))
    let hpp_fns = AuroHppNames(split)
    call OpenOrCreateSrcOrIncFile(hpp_fns)
endfunction

function! c#auro_source_files#OpenImplHppFile()
    let split = AuroSplit(expand('%:p'))
    let impl_cpp_fn = AuroImplHppName(split)
    call OpenOrCreateSingleFile(impl_cpp_fn)
endfunction

function! c#auro_source_files#OpenImplCppFile()
    let split = AuroSplit(expand('%:p'))
    let impl_cpp_fn = AuroImplCppName(split)
    call OpenOrCreateSingleFile(impl_cpp_fn)
endfunction

function! c#auro_source_files#OpenImplTestFile()
    let split = AuroSplit(expand('%:p'))
    let impl_cpp_fn = AuroImplTestName(split)
    call OpenOrCreateSingleFile(impl_cpp_fn)
endfunction

function! c#auro_source_files#FindCurrentFileIncludes()
    let split = AuroSplit(expand('%:p'))
    let ns_part = JoinDir(split.namespaces)
    echom 'nspart: ' . ns_part
    " let regex = "'include.+" . ns_part . '/' . split.file . '.' . split.ext . "\"'"
    let regex = "\"include.+" . split.file . '.' . split.ext . "\""
    echom 'regex: ' . regex
    let cmd = 'Rg ' . regex . ' -tcpp -tc'
    echom 'search cmd: ' . cmd
    " execute 'cd ' . fnamemodify(split.module, ':h')
    execute cmd
    echom cmd
endfunction

function! c#auro_source_files#FindChangeDirToSuperModule()
    let split = AuroSplit(expand('%:p'))
    execute 'cd ' . fnamemodify(split.module, ':h')
    pwd
endfunction

function! c#auro_source_files#FindChangeDirToModule()
    let split = AuroSplit(expand('%:p'))
    execute 'cd ' . split.module
    pwd
endfunction

" Create dictionary from filename with following keys:
" module     = path to module name
" type       = protected, public or test
" namespaces = array of dirs leading up to the filename e.g. ['auro', 'cx', 'v1']
" file       = the filename without path
function! AuroSplit(fn)
    let result = {}
    let result.module     = fnamemodify(a:fn, ':h')
    let result.type       = ""
    let result.namespaces = []
    let result.file       = fnamemodify(a:fn, ':t:r')
    let result.ext        = fnamemodify(a:fn, ':e')

    let stop_dirs = ['src', 'inc', 'private', 'public', 'protected']

    while (index(stop_dirs, result.type) < 0)
        "we don't want the last value result.type will have in this loop, so we do it
        "before assigning the next dir name to it.
        if(result.type != "")
            let result.namespaces = add(result.namespaces, result.type)
        endif
        let temp = result.type
        let result.type = fnamemodify(result.module, ':t')
        if temp == result.type
            break
        endif
        let result.module = fnamemodify(result.module, ':h')
    endwhile
    "we added them from back to front, so reverse
    call reverse(result.namespaces)
    "remove trailing /test if it exists
    if match(result.module, '/test') == len(result.module) - 5
        let result.module = result.module[:-5-1]
    endif
    return result
endfunction

" return c or cpp
function! CxxExt(ext)
    return {'h': 'c', 'c': 'c', 'hpp': 'cpp', 'cpp': 'cpp'}[tolower(a:ext)]
endfunction

" return h or hpp
function! HxxExt(ext)
    return {'c': 'h', 'h': 'h', 'cpp': 'hpp', 'hpp': 'hpp'}[tolower(a:ext)]
endfunction

"There are 2 possible filenames for a header, in public or protected
function! AuroHppNames(auro_split)
    let result = {'public': '', 'protected': ''}

    let file = AuroRemove_tests(a:auro_split.file)
    let file = AuroRemove_Impl(file)

    let ns_part = JoinDir(a:auro_split.namespaces)
    let h_ext = HxxExt(a:auro_split.ext)
    " common part for both public and protected
    let common = ns_part . '/' . file . '.' . h_ext

    let result.public = a:auro_split.module . '/public/' . common
    let result.protected = a:auro_split.module . '/protected/' . common

    return result
endfunction

function! AuroCppName(auro_split)
    let result = ''

    let file = AuroRemove_tests(a:auro_split.file)
    let file = AuroRemove_Impl(file)

    let c_ext = CxxExt(a:auro_split.ext)
    let ns_part = JoinDir(a:auro_split.namespaces)

    let result = a:auro_split.module . '/protected' . '/' . ns_part . '/' . file . '.' . c_ext

    return result
endfunction

function! AuroTestCppName(auro_split)
    " first find corresponding header to see if test should be in 'public' or
    " 'protected'
    let hpp_fns = AuroHppNames(a:auro_split)
    if filereadable(hpp_fns.public)
        let type = 'public'
    else
        let type = 'protected'
    endif

    let file = AuroRemove_tests(a:auro_split.file)
    let file = AuroRemove_Impl(file)

    let ns_part = JoinDir(a:auro_split.namespaces)
    let result = a:auro_split.module . '/test/' . type . '/' . ns_part . '/' . file . '_tests.cpp'
    return result
endfunction

function! AuroImplHppName(auro_split)
    let type = '/protected'
    let ns_part = JoinDir(a:auro_split.namespaces)
    let file = AuroRemove_tests(a:auro_split.file)
    let file = AuroRemove_Impl(file)
    let result = a:auro_split.module . type . '/' . ns_part . '/' . file . 'Impl.hpp'
    return result
endfunction

function! AuroImplCppName(auro_split)
    let type = '/protected'
    let ns_part = JoinDir(a:auro_split.namespaces)
    let file = AuroRemove_tests(a:auro_split.file)
    let file = AuroRemove_Impl(file)
    let result = a:auro_split.module . type . '/' . ns_part . '/' . file . 'Impl.cpp'
    return result
endfunction

function! AuroImplTestName(auro_split)
    let type = '/protected'
    let ns_part = JoinDir(a:auro_split.namespaces)
    let file = AuroRemove_tests(a:auro_split.file)
    let file = AuroRemove_Impl(file)
    let result = a:auro_split.module . '/test/' . type . '/' . ns_part . '/' . file . 'Impl_tests.cpp'
    return result
endfunction

"Removes '_tests' from the file
function! AuroRemove_tests(file)
    let file = a:file
    let file_len = len(file)
    if file_len < 7 
        "cannot be a _tests file
        return file
    endif
    let pos = match(file, "_tests" ) 
    let expected_pos = file_len - 6
    if(pos == expected_pos)
        let file = file[:pos-1]
    endif
    return file
endfunction

function! AuroRemove_Impl(file)
    let file = a:file
    let file_len = len(file)
    if file_len < 5
        return file
    endif
    let pos = match(file,"Impl")
    let expected_pos = file_len - 4
    if(pos == expected_pos)
        let file = file[:pos-1]
    endif
    return file
endfunction

function! OpenOrCreateSingleFile(file)
    if(filereadable(a:file))
        call OpenFile(a:file)
    else
        call inputsave()
        let result = input(a:file . " does not exist, create? (y / n or <esc>): ")
        call inputrestore()
        if result ==? 'y'
            call OpenFile(a:file)
        endif
    endif
endfunction

"Open or create one of the .hxx files in the given dictionary
function! OpenOrCreateSrcOrIncFile(files)
    if !filereadable(a:files.public) && !filereadable(a:files.protected)
        let result = input("Following files do not exist:\ni: " . a:files.public . "\ns: " . a:files.protected . "\nCreate? (i/s/n): ")
        if result ==? 'i' 
            call OpenFile(a:files.public)
        elseif result ==? 's'
            call OpenFile(a:files.protected)
        endif
    elseif filereadable(a:files.protected)
        call OpenFile(a:files.protected)
    elseif filereadable(a:files.public)
        call OpenFile(a:files.public)
    endif
endfunction

"TODO: add option for tab, split, vsplit
"TODO: check if buffer already open, only necessary when noautowrite(all) is
"set (I think)
function! OpenFile(file)
    let containing_dir = fnamemodify(a:file, ':h')
    if(!isdirectory(containing_dir))
        echom 'Creating dir: ' . containing_dir
        call mkdir(containing_dir, 'p')
    endif
    execute ":silent e " . a:file
    "after an edit command, the file does not necessarily exist on disk, we
    "write it so we can find it in subsequent calls to functionality in this
    "file. TODO: first check open buffers, then this write is not necessary
    if(!filereadable(a:file))
        execute ":silent w"
    endif
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

"expand array of dir names to path
function! JoinDir(dir_array)
    let result = ""
    for dir in a:dir_array
        if result != ""
            let result = result . '/'
        endif
        let result = result . dir
    endfor
    return result
endfunction

function! c#auro_source_files#Test()
    "let split = AuroSplit(expand('%'))
    "echom 'Module: ' . split.module . ' * Type: '. split.type . ' * namespaces: ' . split.namespaces[0] .  ' * File: ' . split.file . ' * Ext: ' . split.ext
    "let hpp_names = AuroHppNames(split)
    "echom 'hpp_inc: ' . hpp_names.public . ' * hpp_src: ' . hpp_names.protected
    "let test_name = AuroTestCppName(split)
    "echom 'test_name: ' . test_name

    let split = AuroSplit(expand('%:p'))
    call PrintSplit(split)
    let split.file = AuroRemove_tests(split.file)
    call PrintSplit(split)
endfunction
