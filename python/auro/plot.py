#  import argparse
import pandas as pd
#  from pprint import pprint
import matplotlib.pyplot as plt


#  def parse_args():
#      parser = argparse.ArgumentParser()
#      parser.add_argument(
#          '--input_csv', '-i',
#          default='.',
#          help='csv file with data to plot')
#      return parser.parse_args()


def plot(csv_fn):
    data = pd.read_csv(csv_fn)
    data.plot(y=0)
    plt.title(csv_fn)
    plt.show()


#  if __name__ = '__main__':
#      args = parse_args()
#      fn = args.input_csv


#  plt.plot(x, y, label=fn)
#  plt.xlabel('x')
#  plt.ylabel('y')
#  plt.title('Interesting Graph\nCheck it out')
#  plt.legend()
#  plt.show()
