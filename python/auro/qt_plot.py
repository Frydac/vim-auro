import sys
import json
import socket
import time
import pandas as pd
import numpy as np
import threading
import logging

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

logging.basicConfig(level=logging.INFO)
#  logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#  logging.basicConfig(level=logging.DEBUG)

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        self._canvas = FigureCanvas(Figure(tight_layout=True))
        layout.addWidget(self._canvas)
        self.addToolBar(NavigationToolbar(self._canvas, self))
        self._axes = self._canvas.figure.subplots()

        logging.info("creating tcp server thread")
        self._stop_server_thread = False
        self._tcp_server_thread = threading.Thread(target=self.socket_listener)
        self._tcp_server_thread.start()

    def stop_server(self):
        self._stop_server_thread = True
        logging.debug("stop_server: {}".format(self._stop_server_thread))

    def add_plot_csv(self, csv_fn, name):
        logging.info("add_plot_csv({}, {})".format(csv_fn, name))
        df = pd.read_csv(csv_fn, sep=";", header=None)
        nr_cols = df.shape[1]
        # columns -> plot legend
        df.columns = ["{} (col:{})".format(name, ix) for ix in range(nr_cols)]
        # add plot to existing axes
        df.plot(ax=self._axes)
        # redraw canvas
        self._axes.figure.canvas.draw()

    def socket_listener(self):
        logging.debug("socket_listener")

        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # SO_REUSEADDR reduces (eliminates?) timeout for reuse address when process didn't
        # close the connection properly (e.g. on a crash).
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.bind(('localhost', 50000))
        tcp_server.settimeout(1)
        tcp_server.listen(1)

        def receive_one_msg(conn):
            """:param conn: a valid tcp connection"""

            def parse_data(data):
                logging.debug("data: {}".format(data))
                msg = json.loads(data.decode('utf-8'))
                if 'type' not in msg:
                    logging.error("received json msg has no 'type' key: {}".format(msg))
                elif msg['type'] == 'add_plot_csv':
                    if 'name' not in msg:
                        logging.debug("plot name not set, setting default")
                        msg['name'] = 'no-name-set'
                    return msg
                else:
                    logging.error("msg type not supported: {}".format(msg))
                return None

            def plot_csv_msg(msg):
                if 'csv' in msg:
                    self.add_plot_csv(msg['csv'], msg['name'])
                else:
                    logging.debug("add_plot_csv msg received but no 'csv' key")

            logging.debug("receiving data")
            data = conn.recv(1024)
            logging.debug("received {} bytes".format(len(data)))
            if not data:
                logging.debug("no (valid?) data received")
            else:
                msg = parse_data(data)
                if not msg:
                    return
                if msg['type'] == 'add_plot_csv':
                    plot_csv_msg(msg)

        while not self._stop_server_thread:
            try:
                logging.debug("waiting with socket.accept()")
                conn = None
                conn, addr = tcp_server.accept()
            except socket.timeout:
                logging.debug("timeout")
                continue
            except:
                raise
            else:
                logging.debug("connection accepted")
                receive_one_msg(conn)
            finally:
                if conn:
                    conn.close()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
    app.stop_server()

