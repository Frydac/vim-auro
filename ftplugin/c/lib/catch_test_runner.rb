
require 'pp'

def is_end_path(fn)
    (fn == '/') || (fn.length == 3 && fn[1]=':')
end

# For:
# /home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/comp-hp/test/src/auro/hp/v1_1/Sources_tests.cpp
# returns {basedir: "/home/emile/repos/fusion-cx-ambi-hp-android/fusion-cx-ambi-hp/",
#          module: "comp-hp",
#          test: true,
#          type: "src",
#          namespaces: %w[auro hp v1_1].
#          fn: "Sources_tests.cpp" }
def parse_fn(filename)
    result = {}
    dir, result[:fn] = File.split(filename)
    result[:ext] = File.extname(result[:fn])
    namespace = ""
    result[:namespaces] = []
    stop_dir = ["src", "inc"]
    loop do
        dir, namespace = File.split(dir)
        break if stop_dir.include?namespace
        result[:namespaces] << namespace
        if is_end_path(dir)
            puts("Not a filename I can parse, it does not contain: #{stop_dir}, filename: #{filename}") if is_end_path(dir) #todo:test this on posix/win32
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
    result[:basedir] = dir

    result
end

# Parse a file_tests.cpp file with catch.hpp TEST_CASE() and SECTION() to
# {test_cases:[{line_nr: n, desc: "description", tags: ["tag1", "tag2", ..]},
#              {line_nr: k, desc: "description", tags: ["tag3", "tag4", ..]},
#              ...],
#  sections:{line_number1: {desc: "description", end: line_number_of_closing_bracket},
#            line_number2: {desc: "description", end: line_number_of_closing_bracket},
#            ...}
# }
def parse_catch_test_cpp(file)
    #matches all desc and tags from TEST_CASE line
    test_case_re = /TEST_CASE\(\s*"(.+)"\s*,\s*"\s*(\[.+\])/
    #matches 1 tag from tags match
    test_case_tag_re = /\[(.+?)\]/
    #matches the desc from SECTION line
    section_re = /SECTION\(\s*"(.+)"/

    result = {testcases: [], sections: []}

    File.foreach(file).with_index do |line, line_nr|
        #puts "#{line_nr}: #{line}"

        md_test_case = test_case_re.match(line) #md = match_data
        if md_test_case
            tags_ary_ary = md_test_case[2].scan(test_case_tag_re)
            tags = []
            tags_ary_ary.each do |tag_ary|
                tags << tag_ary[0]
            end
            test_case = {line_nr: line_nr, desc: md_test_case[1], tags: tags}
            result[:testcases] << test_case
            next #we dont need to try and match section
        end

        md_section = section_re.match(line)
        if md_section
            result[:sections] << {line_nr: line_nr, desc: md_section[1]}
            #TODO: find closing bracket and add info
        end
    end
    #pp result
    result
end

def find_test_case(file_info, line_nr)
    last_tc = {}
    file_info[:testcases].each do |tc|
        # find current testcase, i.e. testcase on line before line_nr, or
        # return the first one if line_nr is before first testcase
        last_tc = tc unless last_tc
        if tc[:line_nr] > line_nr
            break
        end
        last_tc = tc
    end
    last_tc
end

def build(fn_info, file_info, line_nr)
    working_dir = fn_info[:basedir]
    cmd = "rake cbs:build[tests-#{fn_info[:module]}]"
    # do it
    cmd = "rake cbs:test[]"
end

module ACR #Auro Catch Runner
    def ACR.run(filename, line_number)

        # parse filename -> get submodule, test_case tag, [section name, [nested section name]]
        fn_info = parse_fn(filename)
        file_info = parse_catch_test_cpp(filename)

        # build target and parse output
        build_output = build(fn_info, file_info, line_number)
        # if error -> construct result and exit
        # run test [tag1][tag2] (or run test -c section_name) and parse output
        # if error -> construct result and exit
        # else return empty dictionary/hash


        # example result

        column_number = 14
        result_list = []
        list_item = {filename: "#{filename}",
                     lnum: line_number,
                     col: column_number,
                     text: "Description",
                     type: 'W'  #error type: in the docs, literally: "single-character error type, 'E', 'W', etc." no clue where to find the etc. part
                    }
        result_list << list_item

        return result_list
    end
end
