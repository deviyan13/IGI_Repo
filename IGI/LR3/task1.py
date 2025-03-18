import math
from inputs import get_valid_input_float


def task1():
    """
    Task 1: Calculate arcsin(x) using Taylor series expansion
    """

    print('Задание 1. Расчет arcsin(x) с помощью ряда Тейлора с точностью eps\n\n')

    # input x
    x = get_valid_input_float(
        prompt='Введите x (|x| < 1): ',
        validation_func=lambda val: abs(val) < 1,
        error_msg='Ошибка: |x| должен быть меньше 1!'
    )
    # input eps
    eps = get_valid_input_float(
        prompt='Введите eps (eps > 0): ',
        validation_func=lambda val: val > 0,
        error_msg='eps должен быть больше 0!'
    )
    n, sum, f_x = custom_arcsin(x, eps)

    # print title
    print(f"{'x':<18} {'n':<3} {'F(x)':<18} {'Math F(x)':<18} {'eps':<10}")
    # print result
    print(f"{x:<18.12f} {n:<3} {sum:<18.16f} {f_x:<18.16f} {eps:<10.7f}")



def custom_arcsin(x, eps):
    """
    Calculate arcsin by Taylor series (max members = 500)
    Args: float x (|x| < 1), float eps (eps > 0)
    Returns n - iterations count, sum - Taylor's sum, f_x - math.asin(x)
    """

    f_x = math.asin(x)
    sum = float(x)
    n = 1
    member = x
    while abs(f_x - sum) > eps:
        member *= (2 * n - 1) ** 2 / (2 * (2 * n + 1) * n)
        member *= x * x
        sum += member
        n += 1
        if n >= 500:
            break

    return n, sum, f_x

task1()