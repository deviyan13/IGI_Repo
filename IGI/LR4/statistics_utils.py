#!/usr/bin/env python3
"""
Statistics Utilities Module
Provides functions to compute arithmetic mean, median, mode, variance, and standard deviation.
"""

import statistics


def arithmetic_mean(data: list) -> float:
    """
    Computes the arithmetic mean of the data.

    Args:
        data (list): List of numeric values.

    Returns:
        float: Arithmetic mean.
    """
    return statistics.mean(data)


def median(data: list) -> float:
    """
    Computes the median of the data.

    Args:
        data (list): List of numeric values.

    Returns:
        float: Median.
    """
    return statistics.median(data)


def mode(data: list) -> float:
    """
    Computes the mode of the data.

    Args:
        data (list): List of numeric values.

    Returns:
        float: Mode (returns NaN if mode is not unique).
    """
    try:
        return statistics.mode(data)
    except statistics.StatisticsError:
        return float('nan')


def variance(data: list) -> float:
    """
    Computes the sample variance of the data.

    Args:
        data (list): List of numeric values.

    Returns:
        float: Variance.
    """
    return statistics.variance(data)


def stdev(data: list) -> float:
    """
    Computes the sample standard deviation of the data.

    Args:
        data (list): List of numeric values.

    Returns:
        float: Standard deviation.
    """
    return statistics.stdev(data)
