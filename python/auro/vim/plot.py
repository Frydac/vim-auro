from pprint import pprint
import json
import os
import re
import socket
import subprocess
import time
import vim


def plot_naft_log_filename_csv(is_new_plot):
    line = vim.current.line
    md = re.match(r'\s*\[data\]\(name:(.*?)\).*\(filename:(.*?)\)', line)
    if not md:
        print("Could not match Dataset ([data](name:...)..(filename:...)) in line: {}".format(line))
        return
    name = md[1]
    fn = md[2]
    cwd = vim.eval("expand('%:p:h')")
    #  fn_plot_script = os.path.join(
    #          os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    #          'plot.py')
    fn_qt_plot_script = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            'qt_plot.py'
            )
    fn_csv = os.path.join(cwd, fn)
    keep_trying = True
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while keep_trying:
        try:
            s.connect(('localhost', 50000))
        except ConnectionRefusedError:
            subprocess.Popen(
                    ['python', fn_qt_plot_script]
                    )
            time.sleep(0.5)
        except:
            keep_trying = False
            raise
        else:
            msg = {'type' : 'plot_csv',
                    'csv': fn_csv,
                    'name': name,
                    'add': str(is_new_plot)}
            s.sendall(json.dumps(msg).encode('utf-8'))
            keep_trying = False

            #  s.sendall()
    #  MyOut = subprocess.Popen(
    #          ['python', fn_plot_script, '-i', fn, '-n', name],
    #          stdout=subprocess.PIPE,
    #          stderr=subprocess.STDOUT)

    # if error, use this to print
    # TODO: put this in a thread
    #  stdout, stderr = MyOut.communicate()
    #  if stderr or stdout:
    #      print("stdout: {}".format(stdout))
    #      print("stderr: {}".format(stderr))
