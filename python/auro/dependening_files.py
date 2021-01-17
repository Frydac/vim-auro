
def re_c_cpp_include(filename):
    return "include\\s*[<\\\"]{}[>\\\"]".format(filename.fn_include())

def re_ruby_require(filename):
    return "require.*{}".format(filename.fn_include_no_ext())

def re_python_import(filename):
    fn_include = '.'.join(filename.namespace_parts()) + ".{}".format(filename.basename.stem)
    #need to escape | for the vim command (pipe), and need to escape \ for the python string.
    return "(from\\|import).*{}".format(fn_include)

def re_include(filename):
    re_include_by_ft = {
            "ruby": re_ruby_require,
            "python": re_python_import,
            "c": re_c_cpp_include,
            "cpp": re_c_cpp_include
            }
    return re_include_by_ft[filename.filetype](filename)

def rg_type_filter(filename):
    rg_type = {
            "ruby": "-truby",
            "python": "-tpy",
            "c": "-tc -tcpp",
            "cpp": "-tc -tcpp",
            }
    return rg_type[filename.filetype]

def rip_grep_cmd_files_including(filename):
    "@param filename: auro.Filename"
    regex = re_include(filename)
    rg_type_filt = rg_type_filter(filename)
    cmd = "Rg -u {} \"{}\"".format(rg_type_filt, regex)
    return cmd


