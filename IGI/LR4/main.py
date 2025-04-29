import re

from task1 import task1
from task2 import task2
from task3 import task3


print()

task1()
task2()
task3()

import abc
class Figure(abc.ABC):
    @abc.abstractmethod
    def area(self): pass

class Color:

    def __init__(self, color : str = 'Black'):
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: str):
        self._color = value