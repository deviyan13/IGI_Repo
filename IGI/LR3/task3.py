def task3():

    print('Задание 3. Определить, является ли введенная с клавиатуры строка двоичным числом\n')

    string = input('Введите строку для проверки, является ли строка двоичным числом:\n')
    if isBinaryNumber(string):
        print('Строка - представление двоичного числа')
    else:
        print('Строка - НЕ представление двоичного числа')

def isBinaryNumber(string):
    for c in string:
        if c != '0' and c != '1':
            return False
    return True

task3()