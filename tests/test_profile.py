#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Francois Boulogne
# License: GPLv3

import unittest
from numpy.testing import assert_almost_equal
import numpy as np

from profile import shooter, calculate_meniscus

def test_height_large_radius():
    for theta in np.linspace(0, 80, 9):
        print('theta %f' % theta)
        # Initial values
        radius = 1e3
        #theta = 0
        delta_z = 1.8

        z, y = shooter(-0.05, 1.55, calculate_meniscus, radius, theta, delta_z, slope_cutoff=2e2)
        assert_almost_equal(z[0], np.sqrt(2) * np.sqrt((1-np.sin(theta * np.pi / 180.))), decimal=2)


