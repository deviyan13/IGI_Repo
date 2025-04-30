"""
Task5
Description:
This program investigates the capabilities of the NumPy library when working with arrays and performing
mathematical/statistical operations. It generates an integer matrix A[n, m] using random numbers.
"""

import numpy as np

from inputs_check import input_int_with_condition


class StatisticsMixin:
    """
    StatisticsMixin provides a helper method to generate a formatted string of statistical
    parameters (arithmetic mean, median, variance, and standard deviation) for a given numpy array.
    """
    @staticmethod
    def get_formatted_statistics(arr: np.ndarray) -> str:
        """
        Returns a formatted string containing statistical parameters for the array.

        Args:
            arr (np.ndarray): Input array.

        Returns:
            str: A formatted multi-line string with statistical parameters.
        """
        if arr.size == 0:
            return "Невозможно вычислить статистику для пустого массива."

        mean_val = arr.mean()
        median_val = np.median(arr)
        var_val = np.var(arr, ddof=1) if arr.size > 1 else 0.0
        std_val = np.std(arr, ddof=1) if arr.size > 1 else 0.0

        stats_str = (
            "Дополнительная общая информация:\n"
            f"Среднее значение: {mean_val:.2f}\n"
            f"Медиана: {median_val:.2f}\n"
            f"Дисперсия: {var_val:.2f}\n"
            f"Стандартное отклонение: {std_val:.2f}\n"
        )
        return stats_str


# --- Class for matrix analysis --- #
class MatrixAnalysis(StatisticsMixin):
    """
    MatrixAnalysis class encapsulates the generation and analysis of a matrix.

    It offers methods to generate an integer matrix using random numbers, compute the arithmetic 
    mean of its elements, select the elements exceeding the mean, and calculate the standard deviation
    of these selected elements in two ways: using NumPy's built-in function and by a manual computation.
    """

    def __init__(self, n: int, m: int):
        """
        Initializes the instance with the given matrix dimensions.

        Args:
            n (int): Number of rows.
            m (int): Number of columns.
        """
        self._n = n
        self._m = m
        self._matrix = None

    @property
    def matrix(self) -> np.ndarray:
        """
        Returns the generated matrix.

        Returns:
            np.ndarray: The matrix.
        """
        return self._matrix

    @matrix.setter
    def matrix(self, value: np.ndarray) -> None:
        """
        Sets the matrix attribute.

        Args:
            value (np.ndarray): A NumPy array to be set as the matrix.
        """
        self._matrix = value

    def generate_matrix(self, low: int = 0, high: int = 101) -> None:
        """
        Generates an integer matrix with dimensions [_n, _m] using random integers in [low, high).

        Args:
            low (int): Lower bound for random integers (inclusive, default 0).
            high (int): Upper bound for random integers (exclusive, default 101).
        """
        self.matrix = np.random.randint(low, high, size=(self._n, self._m))

    def arithmetic_mean(self) -> float:
        """
        Computes the arithmetic mean of all elements in the matrix.

        Returns:
            float: The arithmetic mean.
        """
        return self.matrix.mean()

    def select_exceeding_elements(self) -> np.ndarray:
        """
        Selects and returns the elements of the matrix that are greater than the arithmetic mean.

        Returns:
            np.ndarray: Array of elements exceeding the mean.
        """
        mean_val = self.arithmetic_mean()
        return self.matrix[self.matrix > mean_val]

    def std_builtin(self, arr: np.ndarray) -> float:
        """
        Computes the standard deviation of the given array using NumPy's built-in function.

        Args:
            arr (np.ndarray): Input array.

        Returns:
            float: Standard deviation computed by np.std.
        """

        return np.std(arr, ddof=1) if arr.size > 1 else 0.0

    def std_manual(self, arr: np.ndarray) -> float:
        """
        Computes the standard deviation of the given array manually using the standard formula.
        Formula: sqrt(sum((x - mean)^2) / (N - 1)) for sample standard deviation.

        Args:
            arr (np.ndarray): Input array.

        Returns:
            float: Standard deviation computed manually.
        """
        if arr.size < 2:
            return 0.0
        mean_val = arr.sum() / len(arr)
        squared_diff = (arr - mean_val) ** 2
        variance = squared_diff.sum() / (arr.size - 1)
        return np.sqrt(variance)

    def __str__(self) -> str:
        """
        Returns a formatted string summarizing the analysis results.

        Returns:
            str: Formatted summary string.
        """
        mean_val = self.arithmetic_mean()
        selected = self.select_exceeding_elements()
        count = selected.size
        std_b = self.std_builtin(selected)
        std_m = self.std_manual(selected)
        summary = (
            f"Размер матрицы: {self._n}x{self._m}\n"
            f"Сгенерированная матрица A:\n{self.matrix}\n\n"
            f"Среднее арифметическое элементов матрицы: {mean_val:.2f}\n"
            f"Количество элементов, превосходящих среднее: {count}\n"
            f"Стандартное отклонение (встроенная функция) выборки этих элементов: {std_b:.2f}\n"
            f"Стандартное отклонение (вычислено вручную) выборки этих элементов: {std_m:.2f}"
        )
        return summary


    def get_info(self):
        return self.get_formatted_statistics(self.matrix)

def task5():
    """
    Main function for Task 5.

    It repeatedly prompts the user to enter valid dimensions for the matrix, generates the matrix,
    performs the analysis (selecting elements above the arithmetic mean and calculating their standard
    deviation in two ways), and outputs the results. The user is offered the chance to repeat the process.
    """
    n = input_int_with_condition("Введите количество строк (n > 0): ", lambda x: x > 0)
    m = input_int_with_condition("Введите количество столбцов (m > 0): ", lambda x: x > 0)


    analysis = MatrixAnalysis(n, m)
    analysis.generate_matrix()


    selected_elements = analysis.select_exceeding_elements()
    if selected_elements.size == 0:
        print("Нет элементов, превосходящих среднее значение всей матрицы.")
    else:
        print("\nРезультаты анализа матрицы:")
        print("-" * 60)
        print(analysis)
        print("-" * 60)

    print(analysis.get_info())

if __name__ == '__main__':
    task5()
