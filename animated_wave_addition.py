import sys
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

# Default values and constants
TWOPI = 2 * np.pi
X_MIN = -0.9
X_MAX = 0.9
X_SAMPLES = 1000
F_MIN = 1
F_MAX = 50
F_SAMPLES = F_MAX
TIME_DELAY = 0.5


def plot_wave(x, y):
    """
    Plot a a single (static) wave. Used for diagnostics only.
    :param x: array with x data
    :type x: numpy.ndarray
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
    :type x: numpy.ndarray
    :param frequency_list: array with possible frequencies
    :type frequency_list: list
    :return: sum wave
    :rtype x: numpy.ndarray
    """
    sum_wave = np.zeros(x.size)
    for f in frequency_list:
        y = np.cos(np.pi * f * x)
        sum_wave = np.add(sum_wave, y)
    return sum_wave


def plot_waves(x_min, x_max, x_samples, f_min, f_max, f_samples, time_delay):
    """
    Plot a series of waves. Each wave will be the sum of all the waves for a given frequency range.
    This function iterates over the total number of frequencies, including one more in each iteration.
    The first plot will be a single frequency wave.
    :param x_min: x min
    :type x_min: float
    :param x_max:  x max
    :type x_max: float
    :param x_samples: number of x samples (size of the array)
    :type x_samples: int
    :param f_min: minimum frequency
    :type f_min: float
    :param f_max: maximum frequency
    :type f_max: float
    :param f_samples: number of frequencies
    :type f_samples: int
    :param time_delay: time to wait between plots
    :type time_delay: float
    :return: nothing
    """
    x = np.linspace(x_min, x_max, x_samples)

    frequency_list = np.linspace(f_min, f_max, f_samples)
    # print(frequency_list)

    for n in range(frequency_list.size):
        frequency_slice = frequency_list[0:n + 1]
        # print(frequency_slice)
        sum_wave = calculate_sum_wave(x, frequency_slice)
        # plot_wave(x, sum_wave)
        plt.clf()
        plt.title('Suma de ' + str(frequency_slice.size) + ' Onda(s)')
        plt.ylabel('Amplitud')
        plt.grid(True)
        plt.plot(x, sum_wave)
        plt.pause(time_delay)
    plt.show()


def get_args(argv):
    """
    Process command line arguments
    :param argv: command line arguments from sys.argv
    :type argv: list
    :return: arguments
    :rtype: argparse.Namespace
    """

    parser = ArgumentParser()

    parser.add_argument('--x1',
                        action='store',
                        dest='x1',
                        default=X_MIN,
                        help='x min [default=' + str(X_MIN) + ']')

    parser.add_argument('--x2',
                        action='store',
                        dest='x2',
                        default=X_MAX,
                        help='x max [default=' + str(X_MAX) + ']')

    parser.add_argument('--nx',
                        action='store',
                        dest='nx',
                        default=X_SAMPLES,
                        help='number of x samples [default=' + str(X_SAMPLES) + ']')

    parser.add_argument('--f1',
                        action='store',
                        dest='f1',
                        default=F_MIN,
                        help='minimum frequency (Hz) [default=' + str(F_MIN) + ']')

    parser.add_argument('--f2',
                        action='store',
                        dest='f2',
                        default=F_MAX,
                        help='maximun frequency (Hz) [default=' + str(F_MAX) + ']')

    parser.add_argument('--nf',
                        action='store',
                        dest='nf',
                        default=F_SAMPLES,
                        help='number of frequencies [default=' + str(F_SAMPLES) + ']')

    parser.add_argument('--delay',
                        action='store',
                        dest='delay',
                        default=TIME_DELAY,
                        help='number of frequencies [default=' + str(TIME_DELAY) + ']')

    return parser.parse_args(argv[1:])


if __name__ == '__main__':
    args = get_args(sys.argv)
    plot_waves(float(args.x1), float(args.x2), int(args.nx),
               float(args.f1), float(args.f2), int(args.nf),
               float(args.delay))
