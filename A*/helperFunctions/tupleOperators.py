"""
Functions that do operations for tuples
"""

import numpy as np


def addTuples(a, b):
    """
    Add indices of tuples
    Input: two tuples
    Output: sum of type tuple
    """

    return tuple(np.add(np.array(a), np.array(b)))


def multiplyPower(a, b):
    """
    Multiply indices of tuples with scalar
    Input: tuple, int
    Output: product of type tuple
    """

    return (a[0] * b, a[1] * b)