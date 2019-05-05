import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg = {'type': 'add_plot_csv', 'csv': "/home/emile/repos/toplevel-fusion/cache/generated/core/audio/log_data/1555851405155099_masking_thresholds.csv"}
s.connect(('localhost', 50000))
s.sendall(json.dumps(msg).encode('utf-8'))

    #  app.add_plot_csv("/home/emile/repos/toplevel-fusion/cache/generated/core/audio/log_data/1555851405155099_masking_thresholds.csv", "test")
