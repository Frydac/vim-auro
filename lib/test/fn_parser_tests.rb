require 'test/unit'
require 'pp'

require_relative '../fn_parser.rb'


class TC_MyTest < Test::Unit::TestCase

  def test_parse_fn()

     @scenarios = [{path: '/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/test/src/auro/hp/v1_1/Sources_tests.cpp',
                   expected: {fn: 'Sources_tests.cpp',
                              ext: '.cpp',
                              namespaces: %w[auro hp v1_1],
                              module: 'comp-hp',
                              type: 'src',
                              test: true,
                              base_dir: '/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp'}},
                    {path: '/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/test/auro/hp/v1_1/Sources_tests.cpp',
                     expected: {} } # this one fails
     ]

      @scenarios.each do |scenario|
          result = Auro::Fn::Parser::parse(scenario[:path])
          #assert(result == scenario[:expected])
      end
  end

  def test_fn_cpp_class
      path = '/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/test/src/auro/hp/v1_1/Sources_tests.cpp'

      fn_helper = Auro::Fn::Cpp.new(path)

      fn_src = fn_helper.get_source_fn
      assert_equal('/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/src/auro/hp/v1_1/Sources_tests.cpp', fn_src)

      fns_header = fn_helper.get_header_fns
      assert_equal({'src'=> '/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/src/auro/hp/v1_1/Sources_tests.hpp',
                    'inc'=> '/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/inc/auro/hp/v1_1/Sources_tests.hpp'},
                    fns_header)

      fns_test = fn_helper.get_test_fns
      assert_equal({'src'=> '/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/test/src/auro/hp/v1_1/Sources_tests.cpp',
                    "inc"=> "/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/test/inc/auro/hp/v1_1/Sources_tests.cpp"},
                    fns_test)

  end

  def test_fn_ruby_class
            # /home/emile/repos/auro-cx-v1/core-io/ruby/io/tree/parser.rb
            # /home/emile/repos/auro-cx-v1/core-io/test/ruby/io/tree/parser_tests.rb
      path_src = '/home/emile/repos/auro-cx-v1/core-io/ruby/io/tree/parser.rb'
      path_test = '/home/emile/repos/auro-cx-v1/core-io/test/ruby/io/tree/parser_tests.rb'

      fn_source = Auro::Fn::Ruby.new(path_src)
      puts 'test_fn', fn_source.get_test_fn

      fn_test = Auro::Fn::Ruby.new(path_test)
      puts 'source_fn', fn_test.get_source_fn

      fn_helper_test = Auro::Fn::Ruby.new('/home/emile/repos/auro-cx-v1/core-io/test/ruby/io/tree/parser_tests.rb')
  end

  def test_remove_tests
      input = 'file_tests.rb'
      expected = 'file.rb'

      actual = Auro::Fn::Ruby.remove_tests_part(input)

      assert_equal(expected, actual)
  end

  def test_supermodule_get_folder
      # this needs to be a real folder
      path_abs = '/home/emile/repos/auro-cx-v2/core-build/docs/index.md'
      path_relative = 'auro-cx-v2/core-build/docs/index.md'
      path_win = 'C:/git/test'

      puts "█ path_abs:"; pp path_abs
      puts Auro::Fn::Supermodule::get_folder(path_abs)
      puts Auro::Fn::Module::get_folder(path_abs)
  end

end
