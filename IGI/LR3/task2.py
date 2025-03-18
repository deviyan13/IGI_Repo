from inputs import input_int

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

    print('Количество отрицательных чисел =', result)

task2()