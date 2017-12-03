# vim dependent scripts, can not be unittested (at least without moc'ing vim, I think)
#

module MyVim

    def self.open_ruby_test_file(vim)
        require_relative 'fn_parser.rb'

        fn = Auro::Fn::Ruby::new(current_file_abs_())
        test_fn = fn.get_test_fn
        is_same = test_fn == source_fn
        return if is_same
        MyVim::create_and_open(vim, test_fn)
    end

    def self.open_ruby_source_file(vim)
        require_relative 'fn_parser.rb'

        fn = Auro::Fn::Ruby::new(current_file_abs_())
        source_fn = fn.get_source_fn
        is_same = source_fn == test_fn
        return if is_same
        MyVim::create_and_open(vim, source_fn)
    end

    def self.find_change_dir_to_supermodule(vim)
        require_relative 'fn_parser'
        supermodule_dir = Auro::Fn::Supermodule::get_folder(current_file_abs_(vim))
        vim.command("cd #{supermodule_dir}")
        vim.command("echom '#{supermodule_dir}'")
    end

    def self.find_change_dir_to_module(vim)
        require_relative 'fn_parser'
        module_dir = Auro::Fn::Module::get_folder(current_file_abs_(vim))
        vim.command("cd #{module_dir}")
        vim.command("echom '#{module_dir}'")
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

    private

    def self.current_file_abs_(vim)
        vim.evaluate("expand('%:p')")
    end
end
