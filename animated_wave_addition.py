import numpy as np
import matplotlib.pyplot as plt


def plot_wave(x, y):
    """
    Plot a a single (static) wave. Used for diagnostics only.
    :param x: array with x data
    :param y: array with y data
    :return:
    """
    plt.plot(x, y)
    plt.show()


def calculate_sum_wave(x, frequency_list):
    """
    Calculate the sum of waves for a given frequency range.
    The number of x samples does not need to be the same as the number of frequencies.
    :param x: array with x data
    :param frequency_list: array with possible frequencies
    :return: sum wave
    """
    sum_wave = np.zeros(x.size)
    for f in frequency_list:
        w = 2 * np.pi * f
        y = np.sin(w * x)
        sum_wave = np.add(sum_wave, y)
    return sum_wave


def plot_waves(x_min, x_max, x_samples, f_min, f_max, f_samples):
    """
    Plot a series of waves. Each wave will be the sum of all the waves for a given frequency range.
    This function iterates over the total number of frequencies, including one more in each iteration.
    The first plot will be a single frequency wave.
    :param x_min: x min
    :param x_max:  x max
    :param x_samples: number of x samples (size of the array)
    :param f_min: minimum frequency
    :param f_max: maximum frequency
    :param f_samples: number of frequencies
    :return: nothing
    """
    x = np.linspace(x_min, x_max, x_samples)

    frequency_list = np.linspace(f_min, f_max, f_samples)

    for n in range(frequency_list.size):
        frequency_slice = frequency_list[0:n+1]
        # print(frequency_slice)
        sum_wave = calculate_sum_wave(x, frequency_slice)
        # plot_wave(x, sum_wave)
        plt.clf()
        plt.title('Suma de ' + str(frequency_slice.size) + ' Onda(s)')
        plt.plot(x, sum_wave)
        plt.pause(0.5)
    plt.show()

if __name__ == '__main__':
    max_frequency = 100
    plot_waves(-0.9, 0.9, 1000, 1, max_frequency, max_frequency)

