# vim dependent scripts, can not be unittested (at least without moc'ing vim, I think)
#

module MyVim

    def self.open_ruby_test_file(vim)
        require_relative 'fn_parser.rb'

        source_fn = vim.evaluate("expand('%', ':p')")
        fn = Auro::Fn::Ruby::new(source_fn)
        test_fn = fn.get_test_fn
        is_same = test_fn == source_fn
        return if is_same
        MyVim::create_and_open(vim, test_fn)
    end

    def self.open_ruby_source_file(vim)
        require_relative 'fn_parser.rb'

        test_fn = vim.evaluate("expand('%', ':p')")
        fn = Auro::Fn::Ruby::new(test_fn)
        source_fn = fn.get_source_fn
        is_same = source_fn == test_fn
        return if is_same
        MyVim::create_and_open(vim, source_fn)
    end


    #create file if it doesn't exist after asking for input, and open
    def self.create_and_open(vim, fn)
        fn_exists = File.exists?(fn)

        unless fn_exists
            result = vim.evaluate("input('#{fn} does not exist, create? (y or <esc>): ')")
            if (result == 'y')
                require 'fileutils'
                FileUtils::mkdir_p(File.dirname(fn))
                File.new(fn, 'w')
            else
                # don't create file
                return
            end
        end
        vim.command("execute \":silent e #{fn}\"")
    end
end
