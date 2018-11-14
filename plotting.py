from matplotlib import pyplot as plt
import numpy as np


def plot_x_y(x, y, plot_title, x_label_name, y_label_name, file_name, tick_freq=10):
    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel=x_label_name, ylabel=y_label_name,
           title=plot_title)
    ax.grid()
    plt.xticks(np.arange(min(x), max(x) + 1, tick_freq))
    fig.autofmt_xdate()
    fig.savefig(file_name)
    plt.show()
