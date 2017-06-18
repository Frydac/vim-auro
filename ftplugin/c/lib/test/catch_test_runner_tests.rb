require 'test/unit'

require_relative '../catch_test_runner.rb'
require 'pp'

class TC_MyTest < Test::Unit::TestCase
   def setup
     @fn = "/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/test/src/auro/hp/v1_1/Sources_tests.cpp"
   end

  # def teardown
  # end

  def test_parse_fn()
      result = parse_fn(@fn)
      pp result
      assert(result[:fn] = "Sources_tests.cpp" )
      assert(result[:ext] = ".cpp")
      assert(result[:namespaces] == %w[auro hp v1_1])
      assert(result[:module] == "comp-hp")
      assert(result[:basedir] == "/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp")
      #pp parse_fn("/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/test/auro/hp/v1_1/Sources_tests.cpp")
      #assert(false, 'Assertion was false.')
  end

  def test_parse_catch_test_cpp()
      parse_catch_test_cpp(@fn)
  end

  def test_find_test_case_before_first()
      file_info = parse_catch_test_cpp(@fn)
      testcase = find_test_case(file_info, 1)
      pp 'before first', testcase
  end

  def test_find_test_case_after_first()
      file_info = parse_catch_test_cpp(@fn)
      testcase = find_test_case(file_info, 9)
      pp 'should not be empty', testcase
  end

end
