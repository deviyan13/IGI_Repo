
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