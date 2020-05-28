#!/usr/bin/env python3
import math


def calc_distance(x1, y1, x2, y2):
    """Calculate distance between 2 points."""
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def convert_degree_angle(angle, pos_neg=True):
    """
    Convert angle in degrees from positive to negative or negative to positive.
    :param angle: [float] Angle in degrees.
    :param pos_neg: [bool] If True and angle over 180, converts to negative angle.
                           If False and angle is negative, converts to positive angle.
    :return: [float] Converted angle in degrees.
    """
    if pos_neg:
        return (angle - 360.0) if angle > 180 else angle
    # convert negative to positive
    return angle % 360.0


def average(values):
    """
    Get average of a list of values.
    :param values: list[float] Values used to get average.
    :return: [float] Average of values.
    """
    return sum(values) / len(values)


def weighted_avg(values, power=2):
    """
    Gets weighted average of a list using inverted indices by power (lower indices have highest weight).
    :param values: list[float] Values used to get weighted average.
    :param power: [int] Used in formula to create weighted average.
    :return: [float] Weighted average of values.
    """
    powers = [float(n ** power) for n, _ in enumerate(values)]
    # get inverse of sum to shift weights from highest to lowest
    weights = [n / sum(powers) for n in powers]
    return sum([a * w for a, w in zip(values, weights)])
