from auro.filename import Filename
from pprint import pprint

  #  Build.register_block("QC tests for cli-vst a3deng.v3 - Alternative 3D", :qc, :fast, :cli, :vst, :a3deng, :alt_3d, :v3) do
  #    run_tests_(:alt3d_test, :alt_3d)
  #  end
def ruby_script_type(fn: Filename):
    types = ['story', 'qc', 'script', 'ruby']
    for type in types:
        if type in fn.dirname.dir_part:
            return type
    return 'script_type'

def snip_register_block(fn: Filename):
    type = ruby_script_type(fn)
    module_tags = ", ".join(f":{name}" for name in fn.git_modules()[1]["name"].split('/'))
    result = ""
    result += f"Build.register_block('$1', :{type}, ${{2::fast}}, {module_tags}, $3) do\n"
    result += "    $0\n"
    result += "end\n"
    return result

def snip_register_class(fn: Filename):
    type = ruby_script_type(fn)
    module_tags = ", ".join(f":{name}" for name in fn.git_modules()[1]["name"].split('/'))
    result = ""
    result += f"Build.register_class(${{1:self}}, '$2', :{type}, ${{3::fast}}, {module_tags}, $4) do\n"
    result += "    $0\n"
    result += "end\n"
    return result

def indent_each_line(lines, indent):
    indented_lines = [indent + line for line in lines.splitlines()]
    return "\n".join(indented_lines)

def snip_init_story(fn: Filename):
    result = ""
    result += "namespace :story do\n"
    result += "    task :test do\n"
    result += "         $2\n"
    result += "    end\n"
    result += "end\n"
    return result

def snip_init_qc_register_block(fn):
    name = "FusionAm4hpQcV4ParamSmoothing"
    result = ""
    result += f"module {name}\n"
    result += indent_each_line(snip_register_block(fn), '    ') + "\n"
    result += "end\n"
    return result

def snip_init_qc_register_class(fn):
    result = ""
    return result

def snip_init_script_register_block(fn):
    result = ""
    return result

def snip_init_script_register_class(fn):
    result = ""
    return result

def snip_init_ruby(fn):
    result = ""
    return result
