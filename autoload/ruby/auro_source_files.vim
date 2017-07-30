let s:root_dir = expand('<sfile>:p:h:h:h')

function! ruby#auro_source_files#OpenRubyTestFile()
ruby << EOF
    root_dir = Vim::evaluate("s:root_dir")
    load File.join(root_dir, 'lib/vim_helpers.rb')

    MyVim::open_ruby_test_file(Vim)
EOF
endfunction

function! ruby#auro_source_files#OpenRubySourceFile()
ruby << EOF
    root_dir = Vim::evaluate("s:root_dir")
    load File.join(root_dir, 'lib/vim_helpers.rb')

    MyVim::open_ruby_source_file(Vim)
EOF
endfunction
