import json
import os
import socket
import subprocess
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg = {'type': 'add_plot_csv',
        'csv': "/home/emile/repos/toplevel-fusion/cache/generated/comp/cx/log_data/1557148625498547_audio_data.csv"}

keep_trying = True
while keep_trying:
    try:
        s.connect(('localhost', 50000))
    except ConnectionRefusedError:
        fn_qt_plot = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'qt_plot.py')
        MyOut = subprocess.Popen(
                ['python', fn_qt_plot],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
        time.sleep(0.5)
    except:
        keep_trying = False
        raise
    else:
        s.sendall(json.dumps(msg).encode('utf-8'))
        keep_trying = False
