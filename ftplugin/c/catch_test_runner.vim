
"if exists("catch_test_runner_loaded")
    "finish
"endif
"let catch_test_runner_loaded = 1

command! -buffer AuroCatchTest :call AuroCatchTest()

function! AuroCatchTest()
ruby << EOF

# use :h ruby

fn = Vim::Buffer.current.name
num = Vim::Buffer.current.line_number

puts fn, num



EOF
endfunction

function! AuroSetQFList()
    let buffnr = bufnr('%')
    let filename = expand('%', ':p')
    let line_number = 15
    let pattern = ""
    let col = 5
    let error_number = 1
    let text = "descriptiont of error"
    let error_type = "E"

    echom buffnr
    echom filename
    echom line_number

    let dict = {
                \ 'bufnr': buffnr,
                \ 'filename': filename,
                \ 'lnum': line_number, 
                \ 'col': col,
                \ 'nr': error_number,
                \ 'text': text,
                \ 'type': error_type
                \ }
    echom dict['filename']
    call setqflist([dict])
endfunction

function! AuroSetQFListRuby()
ruby << EOF
    dict = {
        bufnr:  Vim::Buffer::current.number,
        filename: Vim::evaluate("expand('%', ':p')"),
        lnum: 17,
        col: 10,
        nr: 1,
        text: 'descriptive text',
        type: 'W'
    }

    require 'json'

    puts dict.to_json
    Vim::evaluate("setqflist([#{dict.to_json}])")
EOF
endfunction

function! AuroCatchTestBuildRunPrototype()
ruby << EOF
    require_relative 'ftplugin/c/lib/catch_test_runner.rb'
    require 'json'

    filename = Vim::evaluate("expand('%', ':p')")
    line_number = Vim::evaluate("line('.')")

    results_list = ACR::run(filename, line_number)

    puts results_list.to_json
    Vim::evaluate("setqflist(#{results_list.to_json})")
EOF
endfunction

