import random
from inputs import input_int_list


def random_int_generator(size: int, min_val: int = -100, max_val: int = 100):
    """
    Generator for random integers.
    Args:
        size (int): The number of integers to generate.
        min_val (int): The minimum value (default is -100).
        max_val (int): The maximum value (default is 100).
    Yields:
        int: Random integers within the specified range.
    """
    for _ in range(size):
        yield random.randint(min_val, max_val)


def generate_int_sequence(seq: list, size: int, min_val: int = -100, max_val: int = 100):
    """
    Initializes a list with a sequence of random integers using a generator.
    Args:
        seq (list): The list to be initialized.
        size (int): The number of elements to generate.
        min_val (int): The minimum value of the random numbers.
        max_val (int): The maximum value of the random numbers.
    """
    gen = random_int_generator(size, min_val, max_val)  # get a generator instance
    seq[:] = [num for num in gen]  # fill the list with generated numbers

def user_input_init_sequence(seq: list, size: int):
    """
    Initializes the provided list with a sequence of integers entered by the user.
    Args:
        seq (list): The list to be initialized.
        size (int): The number of integers to input.
    Note:
        This function relies on the `input_int_list(size)` function to handle user input.
    """
    seq[:] = input_int_list(size)