
def string_without_words_starts_with(str, letter):
    """
    Removes words that start with a specific letter from a string.
    Args:
        text (str): The input string.
        letter (str): The letter to check words against.
    Returns:
        str: The modified string without words starting with the given letter.
    """

    words = str.replace(',', '').replace('.','').split()
    for word in words:
        if word.lower().startswith(letter):
            str = str.replace(word, '')
    return str


def first_word_contains_letter(str, letter):
    """
    Finds the first word that contains a specific letter.
    Args:
        text (str): The input string.
        letter (str): The letter to search for.
    Returns:
        tuple: The first word containing the letter and its index in the list of words,
               or (None, -1) if no such word is found.
    """

    words = str.replace(',', '').replace('.', '').split()
    for word in words:
        if word.find(letter) != -1:
            return word, words.index(word)
    return None, -1


def get_lower_letters_count(str):
    """
    Counts the number of lowercase letters in a string.
    Args:
        text (str): The input string.
    Returns:
        int: The number of lowercase letters in the string.
    """

    lower_letters = 0

    for c in str:
        if c.islower():
            lower_letters += 1

    return lower_letters
