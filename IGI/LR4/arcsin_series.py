#!/usr/bin/env python3
"""
Arcsin Series Module
This module provides the ArcsinSeries class which computes the Taylor series
approximation for arcsin(x).
"""

import math
from typing import Any, Generator


class ArcsinSeries:
    """
    ArcsinSeries class computes the Taylor series approximation for arcsin(x) using
    the expansion formula:

      arcsin(x) = sum_{k=0}^∞ ( (2k)! / (4^k * (k!)^2 * (2k+1) ) ) * x^(2k+1)

    Attributes:
        x (float): The argument, must satisfy |x| ≤ 1.
    """

    def __init__(self, x: float):
        if not -1 <= x <= 1:
            raise
        self.x = x

    def math_sum(self):
        return math.asin(self.x)

    def series_sum(self, eps: float) -> tuple:
        """
        Calculate arcsin(x) using the Taylor series expansion until the absolute error is less than eps.
        The series has the form:

          arcsin(x) = x + (1/6)*x^3 + (3/40)*x^5 + (5/112)*x^7 + ...

        More generally:
          arcsin(x) = sum_{k=0}^∞ [ (2k)! / (4^k * (k!)^2 * (2k+1) ) ] * x^(2k+1)

        This implementation multiplies the previous term by a correction factor to obtain
        the next term. Up to 500 terms are computed.

        Args:
            x (float): The input value, must satisfy |x| < 1.
            eps (float): The required tolerance (eps > 0).

        Returns:
            tuple: (n, series_sum)
                n (int): Number of terms (iterations) used,
                series_sum (float): Approximation of arcsin(x) computed by Taylor series,
        """
        series_sum = float(self.x)
        n = 1
        term = self.x
        actual_value = self.math_sum()

        while abs(actual_value - series_sum) > eps:
            term *= ((2 * n - 1) ** 2) / (2 * (2 * n + 1) * n)
            term *= self.x * self.x
            series_sum += term
            n += 1
            if n >= 500:
                break
        return n, series_sum


    def get_n_members(self, n: int) -> Generator[float | Any, Any, None]:
        for i in range (0, n):
            yield math.factorial(2 * i) / ((4 ** i) * (math.factorial(i) ** 2) * (2 * i + 1)) * self.x ** (2 * i + 1)