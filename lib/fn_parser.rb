
module Auro
    module Fn

        module Supermodule
            # get left most parent directory that contains .git
            def self.get_folder(filename)
                raise("should be an existing file") unless File.exists?(filename)
                split_path = filename.split(File::SEPARATOR)
                cur_path = ""
                split_path.each do |part|
                    cur_path = File::SEPARATOR if cur_path.empty? and part.empty?
                    cur_path = File.join(cur_path, part)
                    if (File.directory?(cur_path))
                        git_folder = File.join(cur_path, '.git')
                        return cur_path if File.exists?(git_folder)
                    end
                end
                raise("no .git folder found in any of the parent directories of: #{filename}")
            end
        end

        module Module
            # get right most parent directory that contains .git
            def self.get_folder(filename)
                raise("should be an existing file") unless File.exists?(filename)
                cur_path = filename
                begin
                    cur_path, _ = File.split(cur_path)
                    git_folder = File.join(cur_path, '.git')
                    return cur_path if File.exist?(git_folder)
                end while (not cur_path.empty?)
                raise("no .git folder found in any of the parent directories of: #{filename}")
            end
        end

        class Cpp
            def initialize(filename)
                @parts = Fn::Parser::parse(filename)
            end

            # always 1 fn in src folder
            def get_source_fn
                type = 'src'
                basename = File.basename(@parts[:fn], @parts[:ext]) + Cpp::get_source_ext(@parts[:ext])
                File.join(@parts[:base_dir],
                          @parts[:module],
                          type, 
                          @parts[:namespaces],
                          basename)
            end

            # can be in src or inc folder
            def get_header_fns
                fns = {}
                basename = File.basename(@parts[:fn], @parts[:ext]) + Cpp::get_header_ext(@parts[:ext])
                ['src', 'inc'].each do |type|
                    fns[type] = File.join(@parts[:base_dir],
                                          @parts[:module],
                                          type,
                                          @parts[:namespaces],
                                          basename)
                end
                fns
            end

            # can be in src or inc folder
            def get_test_fns
                fns = {}
                basename = File.basename(@parts[:fn], @parts[:ext]) + Cpp::get_source_ext(@parts[:ext])
                ['src', 'inc'].each do |type|
                    fns[type] = File.join(@parts[:base_dir],
                                          @parts[:module],
                                          'test',
                                          type,
                                          @parts[:namespaces],
                                          basename)
                end
                fns
            end

            def get_impl_source_fn
            end

            def get_impl_header_fn
            end

            def get_impl_test_fn
            end

            private

            def self.get_source_ext(ext)
                new_ext = {h: 'c', c: 'c', hpp: 'cpp', cpp: 'cpp'}[ext.tr('.','').to_sym]
                ".#{new_ext}"
            end
            def self.get_header_ext(ext)
                new_ext = {c: 'h', h: 'h', cpp: 'hpp', hpp: 'hpp'}[ext.tr('.','').to_sym]
                ".#{new_ext}"
            end
        end

        class Ruby
            # /home/emile/repos/auro-cx-v1/core-io/ruby/io/tree/parser.rb
            # /home/emile/repos/auro-cx-v1/core-io/test/ruby/io/tree/parser_tests.rb
            def initialize(filename)
                @fn = filename
                @parts = Fn::Parser::parse(filename, stop_dirs = ['ruby'])
            end

            def get_source_fn
                return @fn if @parts[:test] == false
                new_fn = Ruby::remove_tests_part(@parts[:fn])
                File.join(@parts[:base_dir], @parts[:module], 'ruby', @parts[:namespaces], new_fn)
            end

            def get_test_fn
                return @fn if @parts[:test] == true
                File.join(@parts[:base_dir], @parts[:module], 'test', 'ruby', @parts[:namespaces],  "#{@parts[:fn_base]}_tests#{@parts[:ext]}")
            end


            def self.remove_tests_part(fn)
                ext = File.extname(fn)
                base = File.basename(fn, ext)
                tests = '_tests'
                if(base.end_with?(tests))
                    return base[0..-(tests.length+1)] + ext
                end
                fn
            end
        end


        module Parser
            # For:
            # /home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/test/src/auro/hp/v1_1/Sources_tests.cpp
            # returns {base_dir: "/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/",
            #          module: "comp-hp",
            #          test: true,
            #          type: "src",
            #          namespaces: %w[auro hp v1_1].
            #          fn: "Sources_tests.cpp" }
            def self.parse(filename, stop_dirs = %w[src inc])
                result = {}
                dir, result[:fn] = File.split(filename)
                result[:ext] = File.extname(result[:fn])
                result[:fn_base] = File.basename(result[:fn], result[:ext])
                result[:namespaces] = []
                namespace = nil
                loop do
                    dir, namespace = File.split(dir)
                    break if stop_dirs.include? namespace
                    result[:namespaces] << namespace
                    if is_end_path(dir)
                        puts("Not a filename I can parse, it does not contain: #{stop_dirs}, filename: #{filename}") if is_end_path(dir) #todo:test this on posix/win32
                        return {}
                    end
                end
                result[:namespaces].reverse!
                result[:type] = namespace

                dir, test_or_module = File.split(dir)
                if test_or_module == "test"
                    result[:test] = true
                    dir, result[:module] = File.split(dir)
                else
                    result[:test] = false
                    result[:module] = test_or_module
                end
                result[:base_dir] = dir
                result
            end

            def self.is_end_path(fn)
                (fn == '/') || (fn.length == 3 && fn[1]=':')
            end
        end

    end
end
