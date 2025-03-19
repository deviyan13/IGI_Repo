import math
from inputs import input_int, input_int_list, get_valid_input_float
from list_processing import product_of_even_elements, get_last_null_element_index, get_first_null_element_index, sum_of_elements
from string_processing import get_lower_letters_count, first_word_contains_letter, string_without_words_starts_with
from math_functions import custom_arcsin, isBinaryNumber


def task1():
    """
    Task 1: Calculate arcsin(x) using Taylor series expansion
    """

    print('Задание 1. Расчет arcsin(x) с помощью ряда Тейлора с точностью eps')

    # input x
    x = get_valid_input_float(
        prompt='Введите x (|x| < 1): ',
        validation_func=lambda val: abs(val) < 1,
        error_msg='Ошибка: |x| должен быть меньше 1!'
    )
    # input eps
    eps = get_valid_input_float(
        prompt='Введите eps (eps > 0): ',
        validation_func=lambda val: val > 0,
        error_msg='eps должен быть больше 0!'
    )
    n, sum, f_x = custom_arcsin(x, eps)

    # print title
    print(f"{'x':<18} {'n':<3} {'F(x)':<18} {'Math F(x)':<18} {'eps':<10}")
    # print result
    print(f"{x:<18.12f} {n:<3} {sum:<18.16f} {f_x:<18.16f} {eps:<10.7f}\n\n")



def task2():
    is_end = False
    result = 0

    print('Задание 2. Организация икла, принимающего целые числа с клавиатуры\n'
          'и подсчитывающего количество отрицательных чисел.\n'
          'Окончание цикла – ввод числа, большего 100\n')

    while not is_end:
        is_end = False
        integer = input_int('Введите целое число (число > 100 - выход из цикла): ')
        if integer > 100:
            is_end = True
        elif integer < 0:
            result += 1

    print('Количество отрицательных чисел =', result, '\n\n')


def task3():

    print('Задание 3. Определить, является ли введенная с клавиатуры строка двоичным числом\n')

    string = input('Введите строку для проверки, является ли строка двоичным числом:\n')
    if isBinaryNumber(string):
        print('Строка - представление двоичного числа')
    else:
        print('Строка - НЕ представление двоичного числа')

    print('\n')


def task4():
    text = ('So she was considering in her own mind, '
            'as well as she could, '
            'for the hot day made her feel very sleepy and stupid, '
            'whether the pleasure of making a daisy-chain would be worth the trouble '
            'of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.')

    print('''Задание 4. Вариант 2.
            а) определить количество строчных букв в строке;
            б) найти первое слово, содержащее букву 'v' и его номер;
            в) вывести строку, исключив из нее слова, начинающиеся с 's'\n''')

    print('Строка: ', text)

    print('Количество строчных букв в строке:', get_lower_letters_count(text))
    print("Первое слово с буквой 'v' и его номер:", first_word_contains_letter(text, 'v'))
    print("Строка без слов, начинающихся с 's' =", string_without_words_starts_with(text, 's'))

    print('\n')


def task5():
    size = input_int('Введите размер списка: ')
    list = input_int_list(size)

    print('Произведение четных элементов:', product_of_even_elements(list))
    start = get_first_null_element_index(list)
    end = get_last_null_element_index(list)
    if start != -1 and end != -1:
        print('Сумма элементов между первым и последним нулевым элементом', sum_of_elements(list, start, end))
    else:
        print('Ни одного нулевого элемента!')





task1()
task2()
task3()
task4()
task5()