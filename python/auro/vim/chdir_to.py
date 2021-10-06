import vim
from pathlib import PurePath
from auro.path import AuroPath

def chdir_to_current_file_dir():
    path = PurePath(vim.current.buffer.name).parent
    vim.command('silent exec "cd ' + str(path) + '"')
    print("Changed pwd to current file dir: " + str(path))

def chdir_to_module_dir():
    path = AuroPath(vim.current.buffer.name)
    if path.module_dir:
        vim.command('silent exec "cd ' + path.module_dir + '"')
        print("Changed pwd to module dir: " + path.module_dir)
    else:
        print("Didn't change pwd: no git module dir found.")

def chdir_to_supermodule_dir():
    path = AuroPath(vim.current.buffer.name)
    if path.supermodule_dir:
        vim.command('silent exec "cd ' + path.supermodule_dir + '"')
        print("Changed pwd to supermodule dir: " + path.supermodule_dir)
    else:
        print("Didn't change pwd: no supermodule_dir -> trying to change to module dir instead..")
        chdir_to_module_dir()

