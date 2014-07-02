#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Francois Boulogne
# License: GPLv3

__version__ = '0.1'

import numpy as np

from scipy.integrate import odeint
from scipy.optimize import bisect


def meniscus_pin_ode(r, z):
    """
    returns ODE (dr/dz and d2r/dz2) for a meniscus on a pin

    :param r: distance of the liquid-air interface to the pin center
    :param z: altitude

    :return: numpy array
    """
    # r', r''
    return np.array([r[1], z * (1 + r[1]**2)**(3/2.) + (1+r[1]**2) / (r[0])])


def calculate_meniscus(tcl_position, pin_radius, theta=0, delta_z=0.5,
                       num_point=1800, slope_cutoff=1e7):
    """
    Calculate r(z).

    :param tcl_position: z position of the TCL
    :param pin_radius: radius of the pin
    :param theta: contact angle, in degree
    :param delta_z: estimated height difference between TCL and flat interface
    :param num_point: number of points for z
    :param slope_cutoff: maximum abs value for the slope r(z)

    """
    # set space for altitudes
    z = np.linspace(tcl_position, tcl_position - delta_z, num_point)
    # Set the pin radius and the slope of the TCL
    slope = np.tan(theta * np.pi / 180.)
    r_init = np.array([pin_radius, -slope])
    # Solve ODE
    y, out = odeint(meniscus_pin_ode, r_init, z, full_output=True)
    # HACK: remove dirty points
    try:
        idx = np.where(np.abs(y[:, 1]) > slope_cutoff)[0][0]
        y = y[0:idx]
        z = z[0:idx]
    except IndexError:
        pass
    return (z, y)


def shooter(z_min, z_max, f, *args, **kwargs):
    """
    Shooting method to converge to z(infty) = 0

    :param z_min: lower position of the TCL
    :param z_max: higher position of the TCL
    :param f: function returning the interface
    :param args: args of f
    :param kwargs: keyword args of f

    :return: the result of f, at the converged position.
    """
    def end_pos(pos):
        """
        return z[-1], position of the interface at +infty
        """
        return f(pos, *args, **kwargs)[0][-1]

    z_opt = bisect(end_pos, z_min, z_max)
    return f(z_opt, *args, **kwargs)


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    # Initial values
    radius = 1e3
    theta = 50
    delta_z = 1.8

    z, y = shooter(0.25, 1.55, calculate_meniscus, radius, theta, delta_z, slope_cutoff=2e2)

    # Plot
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 10))
    ax1.plot(z, np.abs(y[:, 1]))
    ax1.set_title('slope')
    ax1.set_ylabel('|dr/dz|')
    ax1.set_yscale('log')
    ax1.set_xlabel('z')

    ax2.plot(y[:, 0], z, 'ro')
    ax2.plot(y[:,0], 1.0 * np.exp(-(y[:,0] - radius)))
    ax2.set_title('profile')
    ax2.set_ylabel('z')
    ax2.set_xlabel('r')
    plt.show()
