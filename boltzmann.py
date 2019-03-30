import sys
import math
import matplotlib.pyplot as plt
from argparse import ArgumentParser

# Constants
PI = math.pi  # 3.1415
R = 8.3144598  # Gas constant [J/(K*mol)]
K = 1.38064852e-23  # Boltzmann constant [J/K]

# Molecular masses [Kg/mol]
M_HYDROGEN = 1.00794 / 1000  # Hydrogen
M_OXYGEN = 15.999 / 1000  # Oxygen
M_AIR = 28.97 / 1000  # Air
M_WATER = 18.01528 / 1000  # Water

# Default values for plots
MAX_ENERGY = 25000  # J
MAX_SPEED = 3000  # m/s
NUM_STEPS = 300


def print_constants():
    """
    Auxiliary routine to print all the constants. Used during debugging.
    """
    print('pi', PI)
    print('R', R)
    print('K', K)
    print('M_AIR', M_AIR)
    print('M_WATER', M_WATER)


def velocity_report(mass, temperature):
    """
    Print the most probable, mean and rms speeds of a distribution
    for a given temperature and molecular mass.
    :param mass: molecular mass [Kg]
    :type mass: float
    :param temperature: temperature [K]
    :type temperature: float
    """
    factor = R * temperature / mass
    print('Most probable speed', math.sqrt(2 * factor))
    print('Average speed', math.sqrt(8 * (factor / PI)))
    print('RMS speed', math.sqrt(3 * factor))


def c2k(t):
    """
    Auxiliary routine to convert Celsius to Kelvin
    :param t: temperature [C]
    :type t: float
    :return: temperature [K]
    :rtype: float
    """
    return t + 273.15


def k2c(t):
    """
    Auxiliary routine to convert Kelvin to Celsius
    :param t: temperature [C]
    :type t: float
    :return: temperature [K]
    :rtype: float
    """
    return t - 273.15


def boltzmann_speed(mass, temperature, max_speed, steps):
    """
    Calculate the speed Boltzmann distribution for a given temperature.
    :param mass: molecular mass
    :type mass: float
    :param temperature: temperature [K]
    :type temperature: float
    :param max_speed: maximum energy to plot [J]
    :type max_speed: float
    :param steps: energy steps
    :type steps: int
    :return: energy distribution as a tuple containing the x,y lists
    :rtype: tuple
    """
    x = []
    y = []
    k = 4 * PI * math.pow(mass / (2 * PI * R * temperature), 1.5)
    # print 'k', k
    speed = 0
    delta_speed = float(max_speed) / steps
    while speed < max_speed:
        x.append(speed)
        v2 = speed * speed
        ex = - mass * v2 / (2 * R * temperature)
        # y = k * v2 * math.exp(e) * dv
        y.append(k * v2 * math.exp(ex) * 100)
        speed += delta_speed
    return x, y


def boltzmann_energy(temperature, max_energy, steps):
    """
    Calculate the energy Boltzmann distribution for a given temperature.
    :param temperature: temperature [K]
    :type temperature: float
    :param max_energy: maximum energy to plot [J]
    :type max_energy: float
    :param steps: energy steps
    :type steps: int
    :return: energy distribution as a tuple containing the x,y lists
    :rtype: tuple
    """
    x = []
    y = []
    k = 2 * PI * math.pow(PI * R * temperature, -1.5)
    # print 'k', k
    energy = 0
    delta_energy = float(max_energy) / steps
    while energy < max_energy:
        x.append(energy)
        y.append(k * math.sqrt(energy) * math.exp(-energy / (R * temperature)) * delta_energy * 100)
        energy += delta_energy
    return x, y


def plot(x_list, y_list, title, label, x_label, y_label):
    """
    Auxiliary routine used by plot_speeds and plot_energies to do the actual plotting
    :param x_list: list of x axis values
    :type x_list: list
    :param y_list: list of y axis values
    :type y_list: list
    :param title: plot title
    :type title: str
    :param label: curve label
    :type label: str
    :param x_label: x axis label
    :type x_label: str
    :param y_label: y axis label
    :type y_label: str
    :return:
    """
    l, = plt.plot(x_list, y_list, label=label)
    plt.setp(l, linewidth=3, color='b')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()


def plot_speeds(title, temp_list, mass, max_speed, steps):
    """
    Plot the velocity Boltzmann distribution for a range of temperatures and molecular mass
    :param title: plot title
    :type title: str
    :param temp_list: list of temperatures
    :type temp_list: list
    :param mass: molecular mass
    :type mass: float
    :param max_speed: maximum speed to plot in the 'x' axis
    :type max_speed: float
    :param steps: number of plot steps
    :type steps: int
    """
    for temperature in temp_list:
        x, y = boltzmann_speed(mass, c2k(temperature), max_speed, steps)
        l, = plt.plot(x, y, label=str(temperature) + ' C')
        plt.setp(l, linewidth=1)
        plt.title(title)
        plt.xlabel('[m/s]')
        plt.ylabel('%')
        plt.legend()
    plt.show()


def plot_energies(title, temp_list, max_energy, steps):
    """
    Plot the energy Boltzmann distribution for a range of temperatures
    :param title: plot title
    :type title: str
    :param temp_list: list of temperatures
    :type temp_list: list
    :param mass: molecular mass
    :type mass: float
    :param max_energy: maximum energy to plot in the 'x' axis
    :type max_energy: float
    :param steps: number of plot steps
    :type steps: int
    """
    for temperature in temp_list:
        x, y = boltzmann_energy(c2k(temperature), max_energy, steps)
        l, = plt.plot(x, y, label=str(temperature) + ' C')
        plt.setp(l, linewidth=1)
        plt.title(title)
        plt.xlabel('[Joules]')
        plt.ylabel('%')
        plt.legend()
    plt.show()


def mass_and_title(mass):
    """
    Auxiliary routine to get the molecular mass from a list of possible choices, if possible.
    Otherwise it converts the molecular mass to float and sets the default title to an empty string.
    The title for the plot is determined by the molecular mass if found in the dictionary.
    :param mass: molecular mass
    :type mass: str
    :return: tuple with the molecular mass (float) and the default plot title (str)
    :rtype: tuple
    """
    d = {'hyd': (M_HYDROGEN, 'Hidrogeno'),
         'oxy': (M_OXYGEN, 'Oxigeno'),
         'air': (M_AIR, 'Aire'),
         'wat': (M_WATER, 'Agua')
         }
    if mass == '':
        mass = 'wat'
    if mass in d:
        return d[mass]
    else:
        try:
            return float(mass), ''
        except ValueError:
            raise ValueError('Cannot convert mass "' + str(mass) + '" to float')


def get_args(argv):
    """
    Process command line arguments
    :param argv: command line arguments from sys.argv
    :type argv: list
    :return: arguments
    :rtype: argparse.Namespace
    """
    parser = ArgumentParser()

    parser.add_argument(action='store',
                        dest='temperatures',
                        nargs='+',
                        default=[],
                        help='temperatures [C]')

    parser.add_argument('--energy',
                        action='store_true',
                        dest='energy',
                        default=False,
                        help='plot energy instead of speed?')

    parser.add_argument('--maxenergy',
                        action='store',
                        dest='maxenergy',
                        default=MAX_ENERGY,
                        help='maximum energy to plot [Joules]')

    parser.add_argument('--maxspeed',
                        action='store',
                        dest='maxspeed',
                        default=MAX_SPEED,
                        help='maximum speed to plot [m/s]')

    parser.add_argument('--numsteps',
                        action='store',
                        dest='numsteps',
                        default=NUM_STEPS,
                        help='number of plot steps')

    parser.add_argument('--mass',
                        action='store',
                        dest='mass',
                        default='',
                        help='molecular mass (<value>|hyd|oxy|air|wat) [default=wat]')

    parser.add_argument('--title',
                        action='store',
                        dest='title',
                        default='',
                        help='plot title')

    return parser.parse_args(argv[1:])


if __name__ == '__main__':
    args = get_args(sys.argv)

    # Convert max energy and max speed to float
    try:
        maximum_speed = float(args.maxspeed)
        maximum_energy = float(args.maxenergy)
    except ValueError:
        print('Cannot convert the max energy and/or max speed to float')
        exit(0)

    # The number of steps in the plot is the same for the speed and energy
    num_steps = int(args.numsteps)

    # Get molecular mass and default title
    try:
        molecular_mass, default_title = mass_and_title(args.mass)
    except ValueError as e:
        print(e)
        exit(0)

    # The title will be the default unless set explicitly in the command line
    plot_title = args.title
    if plot_title == '' and default_title != '':
        plot_title = default_title

    # Convert temperatures to float
    try:
        temperature_list = [float(t) for t in args.temperatures]
    except ValueError:
        print('Cannot convert temperature(s) to float')
        exit(0)

    velocity_report(molecular_mass, c2k(temperature_list[0]))

    if args.energy:
        plot_energies(plot_title, temperature_list, maximum_energy, num_steps)
    else:
        plot_speeds(plot_title, temperature_list, molecular_mass, maximum_speed, num_steps)
