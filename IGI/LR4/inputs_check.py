import matplotlib.colors


def input_int(prompt: str) -> int:
    while True:
        print(prompt)
        input_str = input()
        try:
            num = int(input_str)
            break
        except:
            print('Некорректный ввод')

    return num

def input_float(prompt: str) -> float:
    while True:
        print(prompt)
        input_str = input()
        try:
            num = float(input_str)
            break
        except:
            print('Некорректный ввод')

    return num

def input_float_with_condition(prompt: str, validator) -> float:
    while True:
        print(prompt)
        input_str = input()
        try:
            num = float(input_str)
            if (validator(num)):
                break
            else:
                print('Число не удовлетворяет условию')
        except:
            print('Некорректный ввод')

    return num


def input_int_with_condition(prompt: str, validator) -> int:
    while True:
        print(prompt)
        input_str = input()
        try:
            num = int(input_str)
            if (validator(num)):
                break
            else:
                print('Число не удовлетворяет условию')
        except:
            print('Некорректный ввод')

    return num

def input_color_matplotlib(promt: str) -> str:
    while True:
        color = input(promt).strip()
        if color.lower() in matplotlib.colors.CSS4_COLORS:
            return color
        else:
            print('Такого цвета не существует!')