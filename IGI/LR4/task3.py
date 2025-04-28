#!/usr/bin/env python3
"""
Task 3: Arcsin Taylor Series Analysis and Graph Plotting
Program Name: ArcsinSeriesPlotter
Version: 1.0
Developer: Anufryieu Dzianis
Date: 2025-04-27

Description:
This program computes the Taylor series approximation for arcsin(x)
using the ArcsinSeries class. For a range of x values in [-0.99, 0.99],
it calculates both the series approximation (with a specified tolerance eps)
and the exact value computed by math.asin(x). It then plots both curves on one
coordinate system (with different colors), adds axis labels, a legend, and an
annotation, and finally saves the plot to a file.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from arcsin_series import ArcsinSeries  # using your provided ArcsinSeries class
from inputs_check import input_float_with_condition


def task3():
    eps = input_float_with_condition("Введите значение точности eps (дробное от 0 до 1): ", lambda x: 0 < x < 1)

    x_values = np.linspace(-0.99, 0.99, 300)
    series_values = []
    math_values = []

    # For each x value, compute the series approximation and exact value
    for x in x_values:
        try:
            series_obj = ArcsinSeries(x)
            n, approx = series_obj.series_sum(eps)
            series_values.append(approx)
            math_values.append(series_obj.math_sum())
        except Exception as e:
            print(f"Ошибка при вычислении для x = {x}: {e}")
            series_values.append(float('nan'))
            math_values.append(float('nan'))


    plt.figure(figsize=(20, 12))

    plt.plot(x_values, series_values, 'r-', label=f'Ряд Тейлора (eps = {eps})', linewidth=2)

    plt.plot(x_values, math_values, 'b--', label='math.asin(x)', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.title('Сравнение: ряд Тейлора для arcsin(x) и math.asin(x)')
    plt.legend()
    plt.grid(True)

    x_annot = 0.77
    try:
        series_obj_annot = ArcsinSeries(x_annot)
        n_annot, approx_annot = series_obj_annot.series_sum(eps)
        plt.annotate(f'({x_annot:.2f}, {approx_annot:.2f})',
                     xy=(x_annot, approx_annot),
                     xytext=(x_annot + 0.1, approx_annot - 0.2),
                     arrowprops=dict(facecolor='blue', shrink=0.01))
    except Exception as e:
        print(f"Ошибка добавления аннотации: {e}")

    output_filename = 'files/arcsin_plot.png'
    plt.savefig(output_filename)
    print(f"График сохранён в файл: {output_filename}")
    plt.show()