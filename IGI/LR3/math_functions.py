from math import asin

def custom_arcsin(x, eps):
    """
    Calculate arcsin by Taylor series (max members = 500)
    Args: float x (|x| < 1), float eps (eps > 0)
    Returns n - iterations count, sum - Taylor's sum, f_x - math.asin(x)
    """

    f_x = asin(x)
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


def isBinaryNumber(string):
    for c in string:
        if c != '0' and c != '1':
            return False
    return True

