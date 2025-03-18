"""Задание 5. В соответствии с заданием своего варианта составить программу для обработки вещественных списков. Программа должна содержать следующие базовые функции:
1) ввод элементов списка пользователем;
2) проверка корректности вводимых данных;
3) реализация основного задания с выводом результатов;
4) вывод списка на экран.
    2.
Найти произведение элементов с четными номерами и сумму элементов, расположенных между первым и последним нулевыми элементами

"""
import inputs
from list_processing import product_of_even_elements, get_last_null_element_index, get_first_null_element_index, sum_of_elements

def task5():
    size = inputs.input_int('Введите размер списка: ')
    list = inputs.input_int_list(size)

    print(product_of_even_elements(list))
    start = get_first_null_element_index(list)
    end = get_last_null_element_index(list)
    if start != -1 and end != -1:
        print(sum_of_elements(list, start, end))
    else:
        print('Ни одного нулевого элемента!')


task5()

