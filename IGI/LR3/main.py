"""
Lab Work 3: Standard data types, collections, functions, modules in Python.
Description: This program implements 5 tasks from LabWork3
Version: 1.0
Author: Dzianis Anufryieu
Date: 18.03.2025
"""

from tasks_realizations import task1, task2, task3, task4, task5
from inputs import get_valid_input_int

def main():
    is_exit_from_menu = False
    while not is_exit_from_menu:
        print('''Меню:
              1. Выполнить решение задания №1
              2. Выполнить решение задания №2
              3. Выполнить решение задания №3
              4. Выполнить решение задания №4
              5. Выполнить решение задания №5
              6. Выход из программы
              ''')
        choice = get_valid_input_int('Введите номер пункта меню: ',
                            lambda val: val in [1,2,3,4,5,6],
                            "Нет такого пункта в меню")
        match choice:
            case 1: task1()
            case 2: task2()
            case 3: task3()
            case 4: task4()
            case 5: task5()
            case 6:
                is_exit_from_menu = True
                print('Выход из программы...')

if __name__ == "__main__":
    main()