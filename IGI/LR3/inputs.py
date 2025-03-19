"""
This module contains custom functions for validating input
"""


def input_int(msg=''):
    """
    Prompts the user to enter an integer value.
    Args:
        msg (str, optional): A message to display before input is requested. Defaults to an empty string.
    Returns:
        int: The integer value entered by the user.
    """

    if len(msg) != 0:
        print(msg, end = ' ')

    integer = 0
    is_integer = False
    while not is_integer:
        is_integer = True
        try:
            integer = int(input())
        except ValueError:
            print('Введено не челое число! Введите еще раз:')
            is_integer = False

    return integer


def input_float(msg=''):
    """
    Prompts the user to enter a floating-point number.
    Args:
        msg (str, optional): A message to display before input is requested. Defaults to an empty string.
    Returns:
        float: The floating-point number entered by the user.
    """

    if len(msg) != 0:
        print(msg, end = ' ')

    fl = 0
    is_float = False
    while not is_float:
        is_float = True
        try:
            fl = float(input())
        except ValueError:
            print('Введено не дробное число! Введите еще раз:')
            is_float = False

    return fl

def get_valid_input_float(prompt, validation_func, error_msg):
    """
    Universal function for input validation of float number
    Args:
        prompt (str): Input prompt message
        validation_func (callable): Validation function that returns bool
        error_msg (str): Error message for invalid input
    Returns:
        float: Validated input value
    """
    is_correct_input = False
    while not is_correct_input:
        is_correct_input = True
        x = input_float(prompt)
        if not validation_func(x):
            is_correct_input = False
            print(error_msg)

    return x

def get_valid_input_int(prompt, validation_func, error_msg):
    """
    Universal function for input validation of integer number
    Args:
        prompt (str): Input prompt message
        validation_func (callable): Validation function that returns bool
        error_msg (str): Error message for invalid input
    Returns:
        int: Validated input value
    """
    is_correct_input = False
    while not is_correct_input:
        is_correct_input = True
        x = input_int(prompt)
        if not validation_func(x):
            is_correct_input = False
            print(error_msg)

    return x

def input_int_list(size: int):
    """
    Prompts the user to create a list of integers by entering values one by one.
    Args:
        size (int): The number of integers to be entered into the list.
    Returns:
        list: A list containing the integer values provided by the user.
    """

    list = []
    for i in range(size):
        list.append(input_int(f'Введите {i}-й элемент списка (целое число): '))

    return list