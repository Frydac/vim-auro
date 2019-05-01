import argparse
import pandas as pd
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt


def plot(csv_fn, name):
    df = pd.read_csv(csv_fn, sep=";")
    nr_cols = df.shape[1]
    df.columns = ["{} (col:{})".format(name, ix) for ix in range(nr_cols)]
    df.plot()
    plt.title(csv_fn)
    plt.show()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--name', '-n',
        default='name',
        help='name of the data, used in the legend of the plot')
    parser.add_argument(
        '--input_csv', '-i',
        default='.',
        help='csv file with data to plot')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    plot(args.input_csv, args.name)
