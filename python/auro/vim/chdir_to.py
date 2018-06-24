import vim
from pathlib import PurePath
from auro.path import AuroPath

def chdir_to_current_file_dir():
    path = PurePath(vim.current.buffer.name).parent
    print("Changing dir to current file dir")
    vim.command('cd ' + str(path))
    print("pwd: " + str(path))

def chdir_to_module_dir():
    path = AuroPath(vim.current.buffer.name)
    print("Changing dir to module dir")
    if path.module_dir:
        vim.command('cd ' + path.module_dir)
        print("pwd: " + path.module_dir)
    else:
        print("No module_dir")

def chdir_to_supermodule_dir():
    path = AuroPath(vim.current.buffer.name)
    print("Changing dir to supermodule dir")
    if path.supermodule_dir:
        vim.command('cd ' + path.supermodule_dir)
        print("pwd: " + path.supermodule_dir)
    else:
        print("No supermodule_dir")
        chdir_to_module_dir()

