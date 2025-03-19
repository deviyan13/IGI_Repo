def product_of_even_elements(list):
    """
    Calculates the product of elements at even indices in a given list.
    Args:
        lst (list): A list of numeric values.
    Returns:
        int or float: The product of elements at even indices.
    """

    res = 1

    for i in range(0,len(list),2):
        res *= list[i]

    return res

def get_first_null_element_index(list):
    """
    Finds the index of the first zero element in the given list.
    Args:
        lst (list): A list of numeric values.
    Returns:
        int: The index of the first zero, or -1 if no zero is found.
    """

    if 0 in list:
        return list.index(0)
    else:
        return -1

def get_last_null_element_index(list):
    """
    Finds the index of the last zero element in the given list.
    Args:
        lst (list): A list of numeric values.
    Returns:
        int: The index of the last zero, or -1 if no zero is found.
    """

    if 0 in list:
        for i in reversed(range(len(list))):
            if list[i] == 0:
                return i
    else:
        return -1

def sum_of_elements(list, start_index, end_index):
    """
    Calculates the sum of elements in a list within a given index range.
    Args:
        lst (list): A list of numeric values.
        start_index (int): The starting index (inclusive).
        end_index (int): The ending index (inclusive).
    Returns:
        int or float: The sum of elements in the given range.
    """

    sum = 0
    for i in range(start_index, end_index + 1):
        sum += list[i]

    return sum
