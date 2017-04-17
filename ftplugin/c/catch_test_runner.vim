
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
