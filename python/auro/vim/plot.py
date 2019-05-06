import vim
from pprint import pprint
import re
import subprocess
import os


def plot_naft_log_filename_csv():
    line = vim.current.line
    md = re.match(r'\s*\[data\]\(name:(.*?)\).*\(filename:(.*?)\)', line)
    if not md:
        print("Could not match Dataset ([data](name:...)..(filename:...)) in line: {}".format(line))
        return
    name = md[1]
    fn = md[2]
    cwd = vim.eval("expand('%:p:h')")
    fn_plot_script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            'plot.py')
    fn = os.path.join(cwd, fn)
    MyOut = subprocess.Popen(
            ['python', fn_plot_script, '-i', fn, '-n', name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

    # if error, use this to print
    # TODO: put this in a thread
    #  stdout, stderr = MyOut.communicate()
    #  if stderr or stdout:
    #      print("stdout: {}".format(stdout))
    #      print("stderr: {}".format(stderr))
