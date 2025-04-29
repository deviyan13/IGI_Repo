"""
Geometry Module
This module defines the abstract GeometricFigure class, the FigureColor class, and the Rhombus class.
"""

from abc import ABC, abstractmethod


class GeometricFigure(ABC):
    """
    Abstract base class for geometric figures.
    Requires implementation of the area method.
    """

    @abstractmethod
    def area(self) -> float:
        """
        Computes and returns the area of the figure.

        Returns:
            float: Figure area.
        """
        pass


class FigureColor:
    """
    FigureColor class encapsulates the color property for a geometric figure.
    """

    def __init__(self, color: str):
        self._color = color

    @property
    def color(self) -> str:
        """
        Returns the color of the figure.

        Returns:
            str: Color.
        """
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        """
        Sets the figure color.

        Args:
            value (str): New color.
        """
        self._color = value


class Rhombus(GeometricFigure):
    """
    Rhombus class represents a rhombus whose area is (a * b) / 2.

    The rhombus is positioned so that one of its diagonals is horizontal.
    """
    figure_name = "Ромб"

    @classmethod
    def get_figure_name(cls) -> str:
        """
        Returns the name of the geometric figure.

        This method is a class method, meaning it operates on the class level rather than
        on specific instances. It retrieves the name stored in the `figure_name` class attribute.

        Returns:
            str: The name of the geometric figure.
        """
        return cls.figure_name

    def __init__(self, a: float, b: float, color: str):
        """
        Initializes the Rhombus with diagonals a and b and its color.

        Args:
            a (float): Length of the horizontal diagonal.
            b (float): Length of the vertical diagonal.
            color (str): Figure color.
        """
        self.a = a
        self.b = b
        self._figure_color = FigureColor(color)

    @property
    def color(self) -> str:
        """
        Returns the color of the rhombus.

        Returns:
            str: Color.
        """
        return self._figure_color.color

    @color.setter
    def color(self, value: str) -> None:
        """
        Sets the color of the rhombus.

        Args:
            value (str): New color.
        """
        self._figure_color.color = value

    def area(self) -> float:
        """
        Computes the area of the rhombus.

        Returns:
            float: (a * b) / 2.
        """
        return (self.a * self.b) / 2

    def __str__(self) -> str:
        """
        Returns a formatted string with key parameters of the rhombus.

        Returns:
            str: Details including figure type, diagonals, color, and area.
        """
        return ("Фигура: {name}\nДиагонали: a = {a:.2f}, b = {b:.2f}\nЦвет: {color}\nПлощадь: {area:.2f}"
                .format(name=self.figure_name, a=self.a, b=self.b, color=self.color, area=self.area()))
