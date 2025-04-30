"""
Lab Work №4: Python Programming with NumPy, Pandas, and OOP
File: main.py (the main file of the run program)
Version: 1.0
Developer: Anufryieu Dzianis
Date: 2025-04-27

Description:
This script serves as the entry point for the laboratory work, bringing together five main tasks
to demonstrate fundamental and advanced programming concepts in Python. The project showcases:
    - Object-Oriented Programming (OOP) with inheritance, mixins, and abstract classes.
    - Numerical computations and statistical analysis using NumPy.
    - Data processing and indexing with Pandas on a real-world dataset.
    - Graph visualization using Matplotlib.
"""
from inputs_check import input_int_with_condition
from task1 import task1
from task2 import task2
from task3 import task3
from task4 import task4
from task5 import task5
from task6 import task6


def main():
    while True:
        print('''Меню:
              1. Выполнить решение задания №1 (телефонная книга)
              2. Выполнить решение задания №2 (работа с регулярными выражениями)
              3. Выполнить решение задания №3 (работа с графиками)
              4. Выполнить решение задания №4 (рисование ромба)
              5. Выполнить решение задания №5 (работа с матрицей NumPy)
              6. Выполнить решение задания №6 (доп задание с pandas, кибератаки)
              7. Выход из программы
              ''')
        choice = input_int_with_condition('Введите номер пункта меню: ',
                            lambda val: val in range(1, 8))
        match choice:
            case 1: task1()
            case 2: task2()
            case 3: task3()
            case 4: task4()
            case 5: task5()
            case 6: task6()
            case 7:
                print('Выход из программы...')
                break

if __name__ == "__main__":
    main()