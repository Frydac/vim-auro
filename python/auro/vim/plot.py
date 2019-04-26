import vim
#  from pprint import pprint
import re
import subprocess
import os


def plot_naft_log_filename_csv():
    line = vim.current.line
    md = re.match(r'.*\(filename:(.*)\)', line)
    if not md:
        print("Could not find (filename:<fn>) in line: {}".format(line))
        return
    fn = md[1]
    cwd = vim.eval("expand('%:p:h')")
    fn = os.path.join(cwd, fn)
    MyOut = subprocess.Popen(['python', '/home/emile/repos/toplevel-fusion/plot.py', '-i', fn], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)

    # if error, use this to print
    stdout,stderr = MyOut.communicate()
    print(stdout)
    print(stderr)
