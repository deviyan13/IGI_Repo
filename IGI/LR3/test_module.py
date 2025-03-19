from list_processing import *
from math_functions import *
from sequence_initializers import *
from string_processing import *

def main():
    print("\n=== Тестирование list_processing ===")
    # test 1: The product of elements in even positions
    test_list = [2, 3, 4, 5, 6]
    print(f"Список: {test_list}")
    print(f"Произведение на четных индексах: {product_of_even_elements(test_list)}")

    # test 2: Searching for zeros
    zero_list = [1, 0, 2, 0, 3]
    print(f"\nСписок: {zero_list}")
    print(f"Первый ноль: индекс {get_first_null_element_index(zero_list)}")
    print(f"Последний ноль: индекс {get_last_null_element_index(zero_list)}")

    # test 3: The amount in the range
    print(f"\nСумма элементов [1:3]: {sum_of_elements(zero_list, 1, 3)}")

    print("\n=== Тестирование math_functions ===")
    # test 4: Arcsin calculation
    x = 0.5
    eps = 1e-5
    n, taylor, math_val = custom_arcsin(x, eps)
    print(f"\nArcsin({x}) через ряд Тейлора с точностью 0.00001:")
    print(f"Итераций: {n}, Результат: {taylor:.10f}")
    print(f"Math.asin: {math_val:.10f}")

    # test 5: Binary string verification
    binary_str = "101010"
    print(f"\nСтрока '{binary_str}' двоичная? {isBinaryNumber(binary_str)}")

    print("\n=== Тестирование sequence_initializers ===")
    # test 6: Sequence Generation
    seq = []
    generate_int_sequence(seq, 5)
    print(f"\nСгенерированная последовательность: {seq}")

    print("\n=== Тестирование string_processing ===")
    # test 7: Deleting words
    test_str = "Apple banana cherry apple berry"
    letter = 'a'
    result = string_without_words_starts_with(test_str, letter)
    print(f"\nИсходная строка: {test_str}")
    print(f"После удаления слов на '{letter}': {result}")

    # test 8: Searching for a word with a letter
    word, index = first_word_contains_letter(test_str, 'c')
    print(f"\nПервое слово с 'c': '{word}' (индекс {index})")

    # test 9: Counting lowercase letters
    print(f"Количество строчных букв: {get_lower_letters_count(test_str)}")

if __name__ == "__main__":
    main()