import random

def generate_int_sequence(size: int, min_val: int = -100, max_val: int = 100) -> list:
    """
        Generate a list of random integers.
        Args:
            size (int): Number of elements
            min_val (float): Minimum value (int -100)
            max_val (float): Maximum value (int 100)
        Returns:
            list
    """
    return [random.randint(min_val, max_val) for _ in range(size)]