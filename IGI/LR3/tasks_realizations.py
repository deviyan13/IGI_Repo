from decorators import timing_decorator

from inputs import input_int, input_int_list, get_valid_input_float
from list_processing import product_of_even_elements, get_last_null_element_index, get_first_null_element_index, sum_of_elements
from string_processing import get_lower_letters_count, first_word_contains_letter, string_without_words_starts_with
from math_functions import custom_arcsin, isBinaryNumber



@timing_decorator
def task1():
    """
    Function runs the solution of the 1st task
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
    print(f"{'x':<18} {'n':<3} {'F(x)':<18} {'Math F(x)':<18} {'eps':<20}")
    # print result
    print(f"{x:<18.12f} {n:<3} {sum:<18.16f} {f_x:<18.16f} {eps:<20.16f}\n\n")



def task2():
    """
        Function runs the solution of the 2nd task
        Task 2: Organize a loop that accepts integers from the keyboard and counts the number of negative numbers.
        The end of the loop is entering a number greater than 100
    """

    is_end = False
    result = 0

    print('Задание 2. Организация цикла, принимающего целые числа с клавиатуры\n'
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
    """
        Function runs the solution of the 3rd task
        Task 3: Determine whether a string entered from the keyboard is a binary number.
    """

    print('Задание 3. Определить, является ли введенная с клавиатуры строка двоичным числом\n')

    string = input('Введите строку для проверки, является ли строка двоичным числом:\n')
    if isBinaryNumber(string):
        print('Строка - представление двоичного числа')
    else:
        print('Строка - НЕ представление двоичного числа')

    print('\n')


def task4():
    """
        Function runs the solution of the 4th task
        Task 4: A line of text is given in which the words are separated by spaces and commas.
        a) determine the number of lowercase letters;
        b) find the first word containing the letter 'v' and its number;
        c) output the string by excluding the words starting with 's' from it
    """

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
    """
        Function runs the solution of the 5th task
        Task 5: The program contains the following basic functions:
        1) user input of list items;
        2) checking the correctness of the input data;
        3) implementation of the main task with the output of the results;
        4) Display the list on the screen.
        Find the product of the elements with even numbers and
        the sum of the elements located between the first and last zero elements
    """

    size = input_int('Введите размер списка: ')
    list = input_int_list(size)

    print('Произведение четных элементов:', product_of_even_elements(list))
    start = get_first_null_element_index(list)
    end = get_last_null_element_index(list)
    if start != -1 and end != -1:
        print('Сумма элементов между первым и последним нулевым элементом', sum_of_elements(list, start, end))
    else:
        print('Ни одного нулевого элемента!')

